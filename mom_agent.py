import pandas as pd
from datetime import datetime, date, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import yaml

# ============================================================
# LOAD CONFIGURATION
# ============================================================

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
MOM_FILE = config["paths"]["mom_file"]
EXPORT_FOLDER = config["paths"]["export_folder"]

SENDER_EMAIL = config["email"]["sender"]
SMTP_SERVER = config["email"]["smtp_server"]
SMTP_PORT = config["email"]["smtp_port"]
SENDER_PASSWORD = os.getenv("EMAIL_PASS")  # From GitHub Secret

REMINDER_DAYS = config["reminders"]["days_before_deadline"]
REMINDER_TIMES = config["reminders"]["send_times"]

ESC_L1 = config["escalation"]["level1_after_days"]
ESC_L2 = config["escalation"]["level2_after_days"]
ESC_LB = config["escalation"]["boss_mom_after_days"]
EA_DEPT = config["escalation"]["ea_department"]
BOSS_EMAIL = config["escalation"]["boss_email"]

BOSS_MEETING_ID = config["meetings"]["boss_meeting_id"]

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def load_sheet(sheet):
    return pd.read_excel(MOM_FILE, sheet_name=sheet)

def write_sheet(sheet, df):
    with pd.ExcelWriter(MOM_FILE, engine="openpyxl", mode="a", if_sheet_exists="replace") as writer:
        df.to_excel(writer, index=False, sheet_name=sheet)

def log(task_id, action, actor):
    logs = load_sheet("Logs")
    new_id = logs["LogID"].max() + 1 if not logs.empty else 1

    row = {
        "LogID": new_id,
        "TaskID": task_id,
        "Action": action,
        "Timestamp": datetime.now(),
        "Actor": actor
    }

    logs = pd.concat([logs, pd.DataFrame([row])], ignore_index=True)
    write_sheet("Logs", logs)

# ============================================================
# EMAIL SENDER WITH LOGO HEADER
# ============================================================

def send_email(to_email, subject, content_html):
    msg = MIMEMultipart("alternative")
    msg["From"] = SENDER_EMAIL
    msg["To"] = to_email
    msg["Subject"] = subject

    body = f"""
    <div style='text-align:center; margin-bottom:20px;'>
        <img src='{logo_url}' width='130' />
    </div>
    {content_html}
    """

    msg.attach(MIMEText(body, "html"))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SENDER_EMAIL, SENDER_PASSWORD)
        server.send_message(msg)

# ============================================================
# TASK MANAGEMENT
# ============================================================

def add_task(meeting_id, title, details, department, assigned_to, created_by, deadline):
    tasks = load_sheet("Tasks")
    new_id = tasks["TaskID"].max() + 1 if not tasks.empty else 1

    row = {
        "TaskID": new_id,
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

    tasks = pd.concat([tasks, pd.DataFrame([row])], ignore_index=True)
    write_sheet("Tasks", tasks)

    log(new_id, "created", created_by)
    return new_id

def update_task_status(task_id, status, user):
    tasks = load_sheet("Tasks")
    idx = tasks.index[tasks["TaskID"] == task_id][0]

    tasks.loc[idx, "Status"] = status
    tasks.loc[idx, "LastUpdateDate"] = datetime.now()
    tasks.loc[idx, "LastUpdateBy"] = user

    write_sheet("Tasks", tasks)
    log(task_id, status, user)

# ============================================================
# FOLLOW-UP REMINDERS
# ============================================================

def send_reminders():
    tasks = load_sheet("Tasks")
    users = load_sheet("Users")

    today = date.today()

    for _, t in tasks.iterrows():

        if t["Status"] != "pending":
            continue

        days_left = (t["Deadline"] - today).days

        if days_left > REMINDER_DAYS:
            continue

        user = users[users["UserID"] == t["AssignedTo"]].iloc[0]

        subject = f"Reminder: Task {t['TaskID']} – {t['Title']}"
        body = f"""
        <p>Dear {user['Name']},</p>
        <p>This is a reminder that your task:</p>
        <p><b>{t['Title']}</b></p>
        <p>Deadline: <b>{t['Deadline']}</b></p>
        """

        send_email(user["Email"], subject, body)
        log(t["TaskID"], "reminder_sent", "System")

# ============================================================
# ESCALATION ENGINE
# ============================================================

def escalate_tasks():
    tasks = load_sheet("Tasks")
    users = load_sheet("Users")

    today = date.today()

    for _, t in tasks.iterrows():

        if t["Status"] == "completed":
            continue

        days_over = (today - t["Deadline"]).days

        if days_over < ESC_L1:
            continue

        assigned = users[users["UserID"] == t["AssignedTo"]].iloc[0]
        dept = assigned["Department"]
        role = assigned["Role"]

        # Level 1: Executive → Manager
        if role == "Executive" and days_over >= ESC_L1:
            manager = users[(users["Department"] == dept) & (users["Role"] == "Manager")].iloc[0]

            send_email(
                manager["Email"],
                f"ESCALATION: Task {t['TaskID']} overdue",
                f"<p>Executive has not completed the task <b>{t['Title']}</b>.</p>"
            )
            log(t["TaskID"], "escalated_L1", "System")
            continue

        # Level 2: Manager → EA
        if role == "Manager" and days_over >= ESC_L2:
            ea = users[users["Department"] == EA_DEPT].iloc[0]

            send_email(
                ea["Email"],
                f"ESCALATION: Manager-level Task {t['TaskID']} overdue",
                f"<p>Manager has not completed the task <b>{t['Title']}</b>.</p>"
            )
            log(t["TaskID"], "escalated_L2", "System")
            continue

        # Level 3: Boss-MoM escalation
        if t["MeetingID"] == BOSS_MEETING_ID and days_over >= ESC_LB:
            send_email(
                BOSS_EMAIL,
                f"URGENT: Boss-MoM Task {t['TaskID']} overdue",
                f"<p>Task <b>{t['Title']}</b> is pending beyond allowed time.</p>"
            )
            log(t["TaskID"], "escalated_boss", "System")

# ============================================================
# EXPORT PENDING TASK REPORT
# ============================================================

def export_pending():
    tasks = load_sheet("Tasks")
    pending = tasks[tasks["Status"] == "pending"]

    fname = f"{EXPORT_FOLDER}/Pending_{date.today()}.xlsx"
    pending.to_excel(fname, index=False)
    return fname

# ============================================================
# MAIN EXECUTION
# ============================================================

if __name__ == "__main__":
    print("Running MoM Automations...")

    send_reminders()
    escalate_tasks()
    export_pending()

    print("Completed MoM Automation Run.")
