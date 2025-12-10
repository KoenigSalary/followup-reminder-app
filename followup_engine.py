import pandas as pd
import os
from datetime import datetime, timedelta
import yaml
from email_engine import send_email

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]
OWNER_EMAIL = os.getenv("TEST_EMAIL")

def process_followups():
    print("✅ Running MoM Followup Engine")

    df = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    df["Deadline"] = pd.to_datetime(df["Deadline"], errors="coerce")

    today = datetime.today().date()

    for _, row in df.iterrows():
        if row["Status"].lower() != "pending":
            continue

        if pd.isna(row["Deadline"]):
            continue   # ✅ FIXES NaT ERROR

        due = row["Deadline"].date()

        if today >= due:
            subject = f"MoM Follow-Up: {row['Title']}"
            body = f"""
Dear {row['AssignedTo']},

This is a reminder for your pending MoM task:

Task: {row['Title']}
Department: {row['Department']}
Deadline: {row['Deadline'].date()}

Please update your status.

Regards,
Koenig MoM Automation
"""
            send_email(OWNER_EMAIL, subject, body)
