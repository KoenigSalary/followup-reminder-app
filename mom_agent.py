import pandas as pd
from datetime import datetime, date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import imaplib
import email

# ---------------------------------------------------------
# CONFIGURATION
# ---------------------------------------------------------

MOM_FILE = "/Users/praveenchaudhary/Library/CloudStorage/OneDrive-KoenigSolutionsLtd/MoM/MoM_Master.xlsx"
EXPORT_FOLDER = "/Users/praveenchaudhary/Library/CloudStorage/OneDrive-KoenigSolutionsLtd/MoM/Exports/"

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SENDER_EMAIL = "praveen.chaudhary@koenig-solutions.com"
SENDER_PASSWORD = "<your-app-password>"    # Outlook App Password

def load_sheet(sheet_name):
    """Load a sheet from the master Excel file."""
    return pd.read_excel(MOM_FILE, sheet_name=sheet_name)

def write_sheet(sheet_name, df):
    """Write back to a specific sheet in the master file."""
    with pd.ExcelWriter(MOM_FILE, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
        df.to_excel(writer, index=False, sheet_name=sheet_name)

def add_task(meeting_id, title, details, department, assigned_to, created_by, deadline):
    tasks = load_sheet("Tasks")
    new_task_id = tasks["TaskID"].max() + 1 if not tasks.empty else 1
    
    new_row = {
        "TaskID": new_task_id,
        "MeetingID": meeting_id,
        "Title": title,
        "Details": details,
        "Department": department,
        "AssignedTo": assigned_to,
        "CreatedBy": created_by,
        "CreatedDate": date.today(),
        "Deadline": deadline,
        "Status": "pending",
        "LastUpdateDate": None,
        "LastUpdateBy": None
    }
    
    tasks = tasks.append(new_row, ignore_index=True)
    write_sheet("Tasks", tasks)
    log_action(new_task_id, "created", created_by)
    
    return new_task_id

def update_task_status(task_id, new_status, user_id):
    tasks = load_sheet("Tasks")
    idx = tasks.index[tasks["TaskID"] == task_id][0]
    
    tasks.loc[idx, "Status"] = new_status
    tasks.loc[idx, "LastUpdateDate"] = datetime.now()
    tasks.loc[idx, "LastUpdateBy"] = user_id
    
    write_sheet("Tasks", tasks)
    log_action(task_id, new_status, user_id)

def log_action(task_id, action, actor):
    logs = load_sheet("Logs")
    new_id = logs["LogID"].max() + 1 if not logs.empty else 1
    
    new_row = {
        "LogID": new_id,
        "TaskID": task_id,
        "Action": action,
        "Timestamp": datetime.now(),
        "Actor": actor
    }
    
    logs = logs.append(new_row, ignore_index=True)
    write_sheet("Logs", logs)

def send_email(to_email, subject, body):
    msg = MIMEMultipart()
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

def follow_up_tasks():
    tasks = load_sheet("Tasks")
    users = load_sheet("Users")
    
    today = date.today()
    
    for _, task in tasks.iterrows():
        if task["Status"] != "pending":
            continue
        
        assigned_to = int(task["AssignedTo"])
        user = users[users["UserID"] == assigned_to].iloc[0]
        email = user["Email"]
        
        days_left = (task["Deadline"] - today).days
        
        if days_left < 0:
            subject = f"OVERDUE: Task {task['Title']}"
            body = f"""
            <p>Dear {user['Name']},</p>
            <p>Your task <b>{task['Title']}</b> is overdue.</p>
            <p>Deadline: {task['Deadline']}</p>
            <p>Please update immediately.</p>
            """
            send_email(email, subject, body)
            log_action(task["TaskID"], "reminder_sent", "System")
        
        elif days_left <= 2:
            subject = f"Reminder: Task {task['Title']} (due soon)"
            body = f"""
            <p>Dear {user['Name']},</p>
            <p>Your task <b>{task['Title']}</b> is due in {days_left} days.</p>
            """
            send_email(email, subject, body)
            log_action(task["TaskID"], "reminder_sent", "System")

def export_pending_tasks():
    tasks = load_sheet("Tasks")
    users = load_sheet("Users")
    
    tasks = tasks[tasks["Status"] == "pending"]
    tasks = tasks.merge(users, left_on="AssignedTo", right_on="UserID", how="left")
    
    file_path = os.path.join(EXPORT_FOLDER, f"Pending_{date.today()}.xlsx")
    tasks.to_excel(file_path, index=False)
    
    return file_path

def read_incoming_emails():
    """Connects to Outlook inbox and fetches unread task updates."""
    
    mail = imaplib.IMAP4_SSL("outlook.office365.com")
    mail.login(SENDER_EMAIL, SENDER_PASSWORD)
    mail.select("inbox")

    status, messages = mail.search(None, '(UNSEEN)')
    mail_ids = messages[0].split()

    for msg_id in mail_ids:
        status, msg_data = mail.fetch(msg_id, "(RFC822)")
        msg = email.message_from_bytes(msg_data[0][1])

        from_email = email.utils.parseaddr(msg["From"])[1]
        subject = msg["Subject"]
        
        # Extract body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        process_task_update(from_email, subject, body)

    mail.logout()

def interpret_status(body):
    body = body.lower()

    if "done" in body or "completed" in body:
        return "completed"
    if "in progress" in body or "working" in body:
        return "in-progress"
    if "more time" in body or "extension" in body:
        return "delay"
    if "not my task" in body or "wrong person" in body:
        return "wrong-assignee"

    return "unknown"

def process_task_update(sender_email, subject, body):
    users = load_sheet("Users")
    tasks = load_sheet("Tasks")

    # Identify user
    user_row = users[users["Email"] == sender_email]
    if user_row.empty:
        return
    
    user_id = int(user_row["UserID"].iloc[0])

    # Identify Task ID from subject
    task_id = None
    for word in subject.split():
        if word.isdigit():
            task_id = int(word)
            break

    if task_id is None:
        return

    # Interpret status from email body
    status = interpret_status(body)

    if status == "completed":
        update_task_status(task_id, "completed", user_id)
        send_auto_reply(sender_email, task_id, "completed")

    elif status == "in-progress":
        update_task_status(task_id, "in-progress", user_id)
        send_auto_reply(sender_email, task_id, "in-progress")

    elif status == "delay":
        send_auto_reply(sender_email, task_id, "extension-requested")

    elif status == "wrong-assignee":
        send_auto_reply(sender_email, task_id, "reassignment-required")

    else:
        send_auto_reply(sender_email, task_id, "not-understood")

def send_auto_reply(to_email, task_id, status_type):

    if status_type == "completed":
        subject = f"Task {task_id} marked as Completed ✔"
        body = f"""
        <p>Thank you!</p>
        <p>Task <b>{task_id}</b> has been marked as <b>Completed</b>.</p>
        """

    elif status_type == "in-progress":
        subject = f"Task {task_id} marked as In Progress"
        body = f"""
        <p>Update received.</p>
        <p>Task <b>{task_id}</b> recorded as <b>In Progress</b>.</p>
        """

    elif status_type == "extension-requested":
        subject = f"Request noted for Task {task_id}"
        body = f"""
        <p>Your extension request for Task <b>{task_id}</b> has been noted.</p>
        <p>The admin will review it shortly.</p>
        """

    elif status_type == "reassignment-required":
        subject = f"Reassignment requested for Task {task_id}"
        body = f"""
        <p>You've indicated Task <b>{task_id}</b> does not belong to you.</p>
        <p>The task owner will review and reassign.</p>
        """

    else:
        subject = f"Task {task_id} – Unable to understand update"
        body = f"""
        <p>Your update for Task <b>{task_id}</b> could not be interpreted.</p>
        <p>Please reply using keywords: done / in progress / need more time.</p>
        """

    send_email(to_email, subject, body)

if __name__ == "__main__":
    print("Running MoM Automated Agent…")

    read_incoming_emails()      # Process updates from team
    follow_up_tasks()           # Send reminders
    export_pending_tasks()      # Save daily Excel report

    print("Completed.")

def escalate_tasks():
    tasks = load_sheet("Tasks")
    users = load_sheet("Users")
    escalations = load_sheet("Escalations")

    today = date.today()

    for _, task in tasks.iterrows():

        if task["Status"] == "completed":
            continue

        days_overdue = (today - task["Deadline"]).days

        # Skip tasks that are not overdue
        if days_overdue < 2:
            continue

        # Find assigned user
        assigned_user = users[users["UserID"] == task["AssignedTo"]].iloc[0]
        assigned_email = assigned_user["Email"]
        role = assigned_user["Role"]
        dept = assigned_user["Department"]

        task_id = task["TaskID"]

        # ---------------------------------------------------------
        # LEVEL 1 → Executive → escalate to Manager
        # ---------------------------------------------------------
        if role == "Executive" and days_overdue >= 2:
            manager = users[(users["Department"] == dept) & (users["Role"] == "Manager")]
            if not manager.empty:
                manager_email = manager.iloc[0]["Email"]

                subject = f"ESCALATION: Task {task_id} overdue (Executive)"
                body = f"""
                <p>Dear {manager.iloc[0]['Name']},</p>
                <p>The following task is overdue by {days_overdue} days:</p>
                <p><b>{task['Title']}</b></p>
                <p>Please intervene and follow up with the executive.</p>
                """

                send_email(manager_email, subject, body)

                add_escalation(task_id, manager_email, "Executive overdue escalation")

                continue

        # ---------------------------------------------------------
        # LEVEL 2 → Manager → escalate to EA Office
        # ---------------------------------------------------------
        if role == "Manager" and days_overdue >= 4:

            ea = users[users["Department"] == "EA-Director’s Office"]
            if not ea.empty:
                ea_email = ea.iloc[0]["Email"]

                subject = f"ESCALATION: Task {task_id} overdue (Manager)"
                body = f"""
                <p>EA Team,</p>
                <p>Manager has not resolved the following overdue task:</p>
                <p><b>{task['Title']}</b></p>
                <p>Overdue by {days_overdue} days.</p>
                """

                send_email(ea_email, subject, body)

                add_escalation(task_id, ea_email, "Manager overdue escalation")

                continue

        # ---------------------------------------------------------
        # LEVEL 3 → EA → escalate to BOSS (Boss-MoM only)
        # ---------------------------------------------------------
        if task["MeetingID"] == 1:  # Boss MoM – dedicate MeetingID
            if days_overdue >= 1:
                boss_email = "boss@koenig-solutions.com"  # Update or parameterize

                subject = f"URGENT: Boss-MoM Task {task_id} overdue"
                body = f"""
                <p>Dear Sir,</p>
                <p>This Boss-MoM task is overdue:</p>
                <p><b>{task['Title']}</b></p>
                <p>Assigned to: {assigned_user['Name']}</p>
                """

                send_email(boss_email, subject, body)

                add_escalation(task_id, boss_email, "Boss MoM escalation")

def add_escalation(task_id, escalated_to_email, reason):
    esc = load_sheet("Escalations")
    new_id = esc["EscID"].max() + 1 if not esc.empty else 1

    new_row = {
        "EscID": new_id,
        "TaskID": task_id,
        "EscalatedTo": escalated_to_email,
        "EscalatedDate": date.today(),
        "Reason": reason
    }

    esc = pd.concat([esc, pd.DataFrame([new_row])], ignore_index=True)
    write_sheet("Escalations", esc)

if __name__ == "__main__":
    print("Running MoM Automation…")

    read_incoming_emails()
    follow_up_tasks()
    escalate_tasks()
    export_pending_tasks()

    print("Done.")

