import pandas as pd
from datetime import datetime, timedelta
from email_engine import send_email
import yaml

with open("config.yaml") as f:
    config = yaml.safe_load(f)

with open("team_emails.yaml") as f:
    TEAM = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]

def run_followups():
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    today = datetime.today().date()

    for _, row in tasks.iterrows():
        if row["Status"] != "pending":
            continue

        priority = row["Priority"]
        deadline = pd.to_datetime(row["Deadline"]).date()
        last_followup = pd.to_datetime(row["LastFollowUp"]).date() if not pd.isna(row["LastFollowUp"]) else None

        freq_days = {
            "High": 2,
            "Medium": 3,
            "Low": 5
        }.get(priority, 3)

        if last_followup is None or (today - last_followup).days >= freq_days:
            person = row["AssignedTo"]
            email = TEAM.get(person)

            body = f"""
Reminder for pending task:

Task: {row['Title']}
Deadline: {deadline}
Priority: {priority}

Please update your status.
"""

            send_email(
                email,
                f"MoM Follow-Up: {row['Title']}",
                body
            )

            tasks.loc[_,"LastFollowUp"] = today

    tasks.to_excel(MOM_FILE, sheet_name="Tasks", index=False)
