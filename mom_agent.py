import pandas as pd
import os
from datetime import datetime
import yaml

from email_engine import send_email

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]

def add_task(
    meeting_id,
    title,
    details,
    department,
    assigned_to,
    created_by,
    deadline,
    category="Regular"
):
    df = pd.read_excel(MOM_FILE, sheet_name="Tasks")

    new_task = {
        "MeetingID": meeting_id,
        "Title": title,
        "Details": details,
        "Department": department,
        "AssignedTo": assigned_to,
        "CreatedBy": created_by,
        "CreatedDate": datetime.now(),
        "Deadline": deadline,
        "Status": "pending",
        "LastUpdateDate": datetime.now(),
        "LastUpdateBy": created_by,
        "Category": category
    }

    df.loc[len(df)] = new_task

    with pd.ExcelWriter(MOM_FILE, mode="a", engine="openpyxl", if_sheet_exists="overlay") as writer:
        df.to_excel(writer, sheet_name="Tasks", index=False)

    subject = f"New Task Assigned: {title}"
    body = f"""
    Hello {assigned_to},

    A new task has been assigned to you.

    Task ID: {next_task_id}
    Meeting ID: {meeting_id}
    Title: {title}
    Details: {details}
    Deadline: {deadline}

    Regards,
    Koenig MoM System
    """
    send_email(assigned_to, subject, body)

