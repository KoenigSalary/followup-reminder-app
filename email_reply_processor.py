#!/usr/bin/env python3
"""
COMPLETE EMAIL REPLY PROCESSOR
- Reads inbox for task update replies
- Detects keywords: "working", "completed", "delayed", "on hold"
- Updates task status in Excel
- Sends smart auto-acknowledgement emails
- Logs all actions
"""

import os
import re
import imaplib
import email
from email.header import decode_header
from datetime import datetime
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import yaml

# Load configuration
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

# File paths
MOM_FILE = config['paths']['mom_file']

# Email credentials
SMTP_USER = os.getenv('SMTP_USER')
SMTP_PASS = os.getenv('SMTP_PASS')
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.office365.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))

# Keyword detection patterns
KEYWORDS = {
    'in_progress': [
        'working on', 'started', 'in progress', 'begun', 'working',
        'i am working', "i'm working", 'started working'
    ],
    'completed': [
        'completed', 'done', 'finished', 'complete', 'closed',
        'resolved', 'accomplished', 'delivered'
    ],
    'delayed': [
        'delayed', 'delay', 'need more time', 'extension needed',
        'cannot complete', 'running late', 'behind schedule'
    ],
    'on_hold': [
        'on hold', 'hold', 'waiting for', 'dependency', 'blocked',
        'paused', 'pending approval', 'awaiting'
    ]
}

def connect_to_inbox():
    """Connect to Outlook/Office365 inbox via IMAP"""
    try:
        mail = imaplib.IMAP4_SSL('outlook.office365.com')
        mail.login(SMTP_USER, SMTP_PASS)
        mail.select('INBOX')
        print(f"✅ Connected to inbox: {SMTP_USER}")
        return mail
    except Exception as e:
        print(f"❌ Failed to connect to inbox: {e}")
        return None

def extract_task_id(subject):
    """Extract TaskID from email subject like 'Re: New MoM Task Assigned: Task Title' or '[Task-#123]'"""
    # Pattern 1: [Task-#123]
    match = re.search(r'\[Task-#?(\d+)\]', subject, re.IGNORECASE)
    if match:
        return int(match.group(1))
    
    # Pattern 2: Try to find task by matching subject with task titles in Excel
    # This is a fallback - we'll search Excel for matching title
    return None

def detect_status_from_content(body):
    """Detect intended status from email body content"""
    body_lower = body.lower()
    
    # Check each category
    for status, keywords in KEYWORDS.items():
        for keyword in keywords:
            if keyword in body_lower:
                return status
    
    return None

def get_task_by_id(task_id):
    """Get task details from Excel by TaskID"""
    try:
        df = pd.read_excel(MOM_FILE, sheet_name='Tasks')
        task = df[df['TaskID'] == task_id]
        if not task.empty:
            return task.iloc[0].to_dict()
        return None
    except Exception as e:
        print(f"❌ Error reading task {task_id}: {e}")
        return None

def get_task_by_title_match(subject):
    """Find task by matching subject with task titles"""
    try:
        df = pd.read_excel(MOM_FILE, sheet_name='Tasks')
        
        # Clean subject - remove Re:, Fwd:, etc.
        clean_subject = re.sub(r'^(Re:|Fwd:|RE:|FW:)\s*', '', subject, flags=re.IGNORECASE).strip()
        
        # Try to extract task title from subject
        # Pattern: "New MoM Task Assigned: TASK TITLE"
        match = re.search(r'New MoM Task Assigned:\s*(.+)$', clean_subject, re.IGNORECASE)
        if match:
            task_title = match.group(1).strip()
            
            # Find matching task
            for idx, row in df.iterrows():
                if str(row['Title']).strip().lower() == task_title.lower():
                    return row.to_dict()
        
        return None
    except Exception as e:
        print(f"❌ Error matching task by title: {e}")
        return None

def update_task_status(task_id, new_status, update_notes=''):
    """Update task status in Excel"""
    try:
        df = pd.read_excel(MOM_FILE, sheet_name='Tasks')
        
        # Find task
        task_idx = df[df['TaskID'] == task_id].index
        if len(task_idx) == 0:
            print(f"⚠️  Task #{task_id} not found in Excel")
            return False
        
        # Update status
        status_map = {
            'in_progress': 'in-progress',
            'completed': 'completed',
            'delayed': 'delayed',
            'on_hold': 'on-hold'
        }
        
        df.loc[task_idx, 'Status'] = status_map.get(new_status, 'pending')
        df.loc[task_idx, 'LastUpdateDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        if update_notes:
            current_notes = str(df.loc[task_idx, 'Details'].values[0])
            df.loc[task_idx, 'Details'] = f"{current_notes}\n\n[Update {datetime.now().strftime('%Y-%m-%d')}]: {update_notes}"
        
        # Save back to Excel
        with pd.ExcelWriter(MOM_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name='Tasks', index=False)
        
        print(f"✅ Updated Task #{task_id} → {status_map.get(new_status)}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to update task #{task_id}: {e}")
        return False

def send_acknowledgement_email(to_email, task, detected_status, original_reply):
    """Send smart auto-acknowledgement based on detected status"""
    
    status_templates = {
        'in_progress': {
            'subject': f"✅ Status Updated: {task['Title']} - In Progress",
            'body': f"""Dear {task['AssignedTo']},

Thank you for your update.

This is to confirm that your response has been successfully recorded. The status of the following task has been updated to 🟡 In Progress:

━━━━━━━━━━━━━━━━━━━━━━
Task: {task['Title']}
Department: {task['Department']}
Deadline: {task['Deadline']}
━━━━━━━━━━━━━━━━━━━━━━

✅ Please continue working on the task and update us once it is completed.
✅ In case of any challenges, do inform us so we can assist.

Your original response: "{original_reply[:100]}..."

Best regards,
Koenig MoM Automation Team
(System Generated Acknowledgement)"""
        },
        
        'completed': {
            'subject': f"🎉 Task Completed: {task['Title']}",
            'body': f"""Dear {task['AssignedTo']},

Congratulations! Your task has been marked as ✅ Completed.

━━━━━━━━━━━━━━━━━━━━━━
Task: {task['Title']}
Department: {task['Department']}
Completed on: {datetime.now().strftime('%d %B %Y')}
━━━━━━━━━━━━━━━━━━━━━━

Thank you for the timely completion of this task.

Best regards,
Koenig MoM Automation Team
(System Generated Acknowledgement)"""
        },
        
        'delayed': {
            'subject': f"⚠️ Delay Acknowledged: {task['Title']}",
            'body': f"""Dear {task['AssignedTo']},

Thank you for your update.

We have noted that the following task is currently 🟡 Delayed:

━━━━━━━━━━━━━━━━━━━━━━
Task: {task['Title']}
Department: {task['Department']}
Original Deadline: {task['Deadline']}
━━━━━━━━━━━━━━━━━━━━━━

✅ Kindly confirm the reason for the delay.
✅ Let us know if you require any support or assistance to complete this task.
✅ Please share your revised estimated completion date.

Once we receive your feedback, we will update the records accordingly.

Best regards,
Koenig MoM Automation Team
(System Generated Response)"""
        },
        
        'on_hold': {
            'subject': f"⏸️ Task On Hold: {task['Title']}",
            'body': f"""Dear {task['AssignedTo']},

Thank you for your update.

The following task has been marked as ⚠️ On Hold:

━━━━━━━━━━━━━━━━━━━━━━
Task: {task['Title']}
Department: {task['Department']}
Original Deadline: {task['Deadline']}
━━━━━━━━━━━━━━━━━━━━━━

✅ Please confirm the exact reason for putting the task on hold.
✅ Let us know if you need any help to resolve the dependency.
✅ Inform us when the blocker is cleared so we can reactivate the task.

We're here to support you in removing any obstacles.

Best regards,
Koenig MoM Automation Team
(System Generated Response)"""
        }
    }
    
    template = status_templates.get(detected_status)
    if not template:
        print(f"⚠️  No template for status: {detected_status}")
        return False
    
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = template['subject']
        
        msg.attach(MIMEText(template['body'], 'plain'))
        
        # Send email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()
        
        print(f"✅ Sent acknowledgement to {to_email}")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send acknowledgement: {e}")
        return False

def process_email_replies():
    """Main function to process email replies"""
    print("=" * 70)
    print("📧 EMAIL REPLY PROCESSOR - STARTED")
    print("=" * 70)
    
    mail = connect_to_inbox()
    if not mail:
        return
    
    try:
        # Search for unread emails
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        
        if not email_ids:
            print("✅ No unread emails to process")
            return
        
        print(f"📬 Found {len(email_ids)} unread email(s)")
        
        processed_count = 0
        
        for email_id in email_ids:
            try:
                # Fetch email
                status, msg_data = mail.fetch(email_id, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                
                # Decode subject
                subject = decode_header(msg['Subject'])[0][0]
                if isinstance(subject, bytes):
                    subject = subject.decode()
                
                from_email = msg.get('From')
                
                print(f"\n📨 Processing: {subject[:60]}...")
                
                # Extract email body
                body = ""
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                
                # Extract TaskID
                task_id = extract_task_id(subject)
                
                # If no TaskID in subject, try matching by title
                task = None
                if task_id:
                    task = get_task_by_id(task_id)
                else:
                    task = get_task_by_title_match(subject)
                    if task:
                        task_id = task['TaskID']
                
                if not task:
                    print(f"⚠️  Could not match email to any task")
                    continue
                
                # Detect status from body
                detected_status = detect_status_from_content(body)
                
                if not detected_status:
                    print(f"⚠️  No status keyword detected in email body")
                    continue
                
                print(f"✅ Detected status: {detected_status}")
                
                # Update task status
                update_notes = f"Email reply: {body[:100]}..."
                if update_task_status(task_id, detected_status, update_notes):
                    # Send acknowledgement
                    send_acknowledgement_email(from_email, task, detected_status, body[:200])
                    processed_count += 1
                
            except Exception as e:
                print(f"❌ Error processing email: {e}")
                continue
        
        print(f"\n✅ Processed {processed_count} email(s) successfully")
        
    except Exception as e:
        print(f"❌ Error in email processing: {e}")
    
    finally:
        mail.close()
        mail.logout()
    
    print("=" * 70)
    print("📧 EMAIL REPLY PROCESSOR - COMPLETE")
    print("=" * 70)

if __name__ == "__main__":
    process_email_replies()
