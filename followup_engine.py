import pandas as pd
from datetime import datetime, timedelta
import os
from email_engine import send_email
from config_loader import load_config

config = load_config()

MOM_FILE = "MoM_Master.xlsx"
OWNER_EMAIL = "praveen.chaudhary@koenig-solutions.com"

def should_send_followup(priority, last_followup_date):
    today = datetime.now().date()

    rules = {
        "HIGH": 2,
        "MEDIUM": 3,
        "LOW": 5
    }

    days = rules.get(priority.upper(), 3)

    if pd.isna(last_followup_date):
        return True

    return (today - last_followup_date.date()).days >= days


def run_followup_engine():
    df = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    df.columns = df.columns.str.strip()

    today = datetime.now().date()
    updates = []

    for i, row in df.iterrows():
        if row["Status"] == "completed":
            continue

        priority = row.get("Priority", "MEDIUM")
        last_followup = row.get("LastFollowupDate")

        if should_send_followup(priority, last_followup):

            subject = f"Follow-Up: {row['Title']}"
            body = f"""
Hello,

This is a reminder for your pending task:

Task: {row['Title']}
Department: {row['Department']}
Deadline: {row['Deadline']}
Priority: {priority}

Please update the status.

Regards,
MoM Automation Agent
            """

            send_email(
                OWNER_EMAIL,        # ✅ test mode final (only your email)
                subject,
                body
            )

            df.at[i, "LastFollowupDate"] = today
            updates.append(row["TaskID"])

    df.to_excel(MOM_FILE, sheet_name="Tasks", index=False)

    print("Follow-up sent for Tasks:", updates)


if __name__ == "__main__":
    run_followup_engine()
