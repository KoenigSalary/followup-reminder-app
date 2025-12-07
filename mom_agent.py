import pandas as pd
from datetime import datetime
import yaml
import os

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]

def add_task(meeting_id, title, details, department, assigned_to, created_by, deadline):

    df = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    df.columns = df.columns.str.strip()

    new_id = int(df["TaskID"].max()) + 1 if not df.empty else 1

    new_row = {
        "TaskID": new_id,
        "MeetingID": meeting_id,
        "Title": title,
        "Details": details,
        "Department": department,
        "AssignedTo": assigned_to,
        "CreatedBy": created_by,
        "CreatedDate": datetime.now(),
        "Deadline": deadline,
        "Status": "pending",
        "LastUpdateDate": "",
        "LastUpdateBy": ""
    }

    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(MOM_FILE, sheet_name="Tasks", index=False)

    return new_id

def followup_team_members():

    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    tasks.columns = tasks.columns.str.strip()
    tasks["Deadline"] = pd.to_datetime(tasks["Deadline"], errors="coerce")

    today = date.today()

    pending = tasks[(tasks["Status"] == "pending")]

    for _, row in pending.iterrows():

        task = row["Title"]
        deadline = row["Deadline"]

        body = f"""
Follow-up Reminder (TEST MODE)

Task: {task}
Deadline: {deadline}

Please update the status.
"""

        send_email(
            TEST_EMAIL,
            f"MoM Follow-up Reminder – {task}",
            body
        )


if __name__ == "__main__":
    followup_team_members()


