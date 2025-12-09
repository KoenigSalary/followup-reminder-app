#!/usr/bin/env python3
"""
Email Reply Processor for MoM Agent
Reads incoming emails, detects task updates, and updates the database.
"""

import imaplib
import email
from email.header import decode_header
import pandas as pd
import yaml
import os
import re
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Load configuration
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

# FIX: Use 'paths' instead of 'files'
MOM_FILE = config['paths']['mom_file']
EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS') or os.getenv('SMTP_PASS')

# Keywords to detect task completion
COMPLETION_KEYWORDS = [
    'completed', 'done', 'finished', 'complete', 'closed',
    'resolved', 'delivered', 'submitted', 'updated'
]

PROGRESS_KEYWORDS = [
    'in progress', 'working on', 'will update', 'in process',
    'ongoing', 'started', 'wip', 'will complete by'
]

def connect_to_inbox():
    """Connect to email inbox via IMAP"""
    try:
        # Connect to Outlook/Office365 IMAP
        imap = imaplib.IMAP4_SSL('outlook.office365.com')
        imap.login(EMAIL_USER, EMAIL_PASS)
        imap.select('INBOX')
        return imap
    except Exception as e:
        print(f"❌ Error connecting to inbox: {e}")
        return None

def decode_subject(subject):
    """Decode email subject"""
    try:
        decoded = decode_header(subject)[0]
        if isinstance(decoded[0], bytes):
            return decoded[0].decode(decoded[1] or 'utf-8')
        return decoded[0]
    except:
        return subject

def extract_task_id_from_subject(subject):
    """Extract TaskID from email subject"""
    # Look for patterns like [Task-#123] or Task ID: 123
    patterns = [
        r'\[Task-#(\d+)\]',
        r'Task-(\d+)',
        r'TaskID[:\s]+(\d+)',
        r'Task\s+ID[:\s]+(\d+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, subject, re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None

def detect_status_from_body(body):
    """Detect task status from email body"""
    body_lower = body.lower()
    
    # Check for completion
    for keyword in COMPLETION_KEYWORDS:
        if keyword in body_lower:
            return 'completed'
    
    # Check for in progress
    for keyword in PROGRESS_KEYWORDS:
        if keyword in body_lower:
            return 'in-progress'
    
    return None

def send_auto_reply(to_email, task_title, task_id, new_status):
    """Send automated response to team member"""
    try:
        # Import send_email from mom_agent
        from mom_agent import send_email
        
        subject = f"✅ Task Update Confirmed - [Task-#{task_id}]"
        
        if new_status == 'completed':
            body = f"""
Dear Team,

Thank you for your update! Your task has been marked as COMPLETED ✅

📋 Task Details:
• Task ID: {task_id}
• Title: {task_title}
• Status: Completed
• Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}

Your progress has been recorded in the MoM tracking system.

Best regards,
MoM Automation Agent
            """
        else:  # in-progress
            body = f"""
Dear Team,

Thank you for your update! Your task status has been updated to IN PROGRESS 🔄

📋 Task Details:
• Task ID: {task_id}
• Title: {task_title}
• Status: In Progress
• Updated: {datetime.now().strftime('%d %b %Y %I:%M %p')}

Please keep us updated on your progress.

Best regards,
MoM Automation Agent
            """
        
        send_email(to_email, subject, body)
        return True
    except Exception as e:
        print(f"❌ Error sending auto-reply: {e}")
        return False

def update_task_status(task_id, new_status, reply_text):
    """Update task status in Excel"""
    try:
        df = pd.read_excel(MOM_FILE, sheet_name='Tasks')
        
        # Find the task
        mask = df['TaskID'] == task_id
        if mask.any():
            df.loc[mask, 'Status'] = new_status
            df.loc[mask, 'LastUpdateDate'] = datetime.now()
            
            # Add UpdateNotes column if it doesn't exist
            if 'UpdateNotes' not in df.columns:
                df['UpdateNotes'] = ''
            df.loc[mask, 'UpdateNotes'] = reply_text[:200]  # Store first 200 chars
            
            # Write back to Excel
            with pd.ExcelWriter(MOM_FILE, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name='Tasks', index=False)
            
            print(f"✅ Updated Task #{task_id} to '{new_status}'")
            return True
        else:
            print(f"⚠️ Task #{task_id} not found in database")
            return False
            
    except Exception as e:
        print(f"❌ Error updating task: {e}")
        return False

def process_inbox_replies():
    """Main function to process email replies"""
    print("=" * 60)
    print("🔍 Email Reply Processor Starting...")
    print("=" * 60)
    
    imap = connect_to_inbox()
    if not imap:
        return
    
    try:
        # Search for unread emails
        status, messages = imap.search(None, 'UNSEEN')
        
        if status != 'OK':
            print("❌ No unread messages found")
            return
        
        email_ids = messages[0].split()
        
        if len(email_ids) == 0:
            print("📭 No unread emails in inbox")
            return
            
        print(f"📬 Found {len(email_ids)} unread email(s)")
        
        for email_id in email_ids:
            # Fetch email
            status, msg_data = imap.fetch(email_id, '(RFC822)')
            
            if status != 'OK':
                continue
            
            # Parse email
            msg = email.message_from_bytes(msg_data[0][1])
            subject = decode_subject(msg['Subject'])
            from_email = msg['From']
            
            print(f"\n📧 Processing: {subject}")
            print(f"   From: {from_email}")
            
            # Extract TaskID from subject
            task_id = extract_task_id_from_subject(subject)
            
            if not task_id:
                print(f"   ⚠️ No TaskID found in subject - skipping")
                continue
            
            print(f"   🆔 TaskID: {task_id}")
            
            # Extract email body
            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == "text/plain":
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Detect status from body
            new_status = detect_status_from_body(body)
            
            if new_status:
                print(f"   ✅ Detected status: {new_status}")
                
                # Update database
                success = update_task_status(task_id, new_status, body)
                
                if success:
                    # Get task details
                    df = pd.read_excel(MOM_FILE, sheet_name='Tasks')
                    task = df[df['TaskID'] == task_id].iloc[0]
                    
                    # Send auto-reply
                    reply_sent = send_auto_reply(from_email, task['Title'], task_id, new_status)
                    if reply_sent:
                        print(f"   📤 Auto-reply sent")
                
                # Mark as read
                imap.store(email_id, '+FLAGS', '\\Seen')
            else:
                print(f"   ⚠️ No status keywords detected - skipping")
        
        print("\n✅ Email processing completed")
        
    except Exception as e:
        print(f"❌ Error processing inbox: {e}")
    
    finally:
        imap.close()
        imap.logout()

if __name__ == '__main__':
    process_inbox_replies()
