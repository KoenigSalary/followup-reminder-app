import pandas as pd
from datetime import date
from email_engine import send_email

OWNER_EMAIL = "praveen.chaudhary@koenig-solutions.com"
MOM_FILE = "MoM_Master.xlsx"

def send_daily_summary():
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    tasks.columns = tasks.columns.str.strip()

    completed = len(tasks[tasks["Status"] == "completed"])
    pending = len(tasks[tasks["Status"] == "pending"])
    overdue = len(
        tasks[
            (pd.to_datetime(tasks["Deadline"]) < pd.to_datetime(date.today())) &
            (tasks["Status"] == "pending")
        ]
    )

    body = f"""
📊 DAILY MoM SUMMARY – {date.today()}

✅ Completed: {completed}
⏳ Pending: {pending}
🔥 Overdue: {overdue}

This is your FINAL MODE summary.
"""

    send_email(
        OWNER_EMAIL,
        f"📊 Daily MoM Summary – {date.today()}",
        body
    )

if __name__ == "__main__":
    send_daily_summary()
