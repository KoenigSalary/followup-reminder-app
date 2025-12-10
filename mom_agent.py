import pandas as pd
import os
from datetime import datetime
import yaml

from email_engine import send_email

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]

def add_task(meeting_id, title, details, department, assigned_to, created_by, deadline, category):
    import pandas as pd
    from datetime import datetime

    file_path = "MoM_Master.xlsx"
    df = pd.read_excel(file_path, sheet_name="Tasks")

    # ✅ ENSURE ALL REQUIRED COLUMNS EXIST
    required_cols = [
        "TaskID", "MeetingID", "Title", "Details", "Department",
        "AssignedTo", "Status", "CreatedDate", "Deadline",
        "LastUpdateDate", "CreatedBy", "Category"
    ]

    for col in required_cols:
        if col not in df.columns:
            df[col] = ""

    # ✅ FORCE CORRECT COLUMN ORDER
    df = df[required_cols]

    # ✅ AUTO-GENERATE PROPER TASK ID
    if df["TaskID"].dropna().empty:
        next_task_id = 1
    else:
        df["TaskID"] = pd.to_numeric(df["TaskID"], errors="coerce")
        next_task_id = int(df["TaskID"].max()) + 1

    # ✅ CREATE NEW ROW WITH CORRECT MAPPING
    new_task = {
        "TaskID": next_task_id,
        "MeetingID": meeting_id,
        "Title": title,
        "Details": details,
        "Department": department,
        "AssignedTo": assigned_to,
        "Status": "pending",
        "CreatedDate": datetime.now(),
        "Deadline": deadline,
        "LastUpdateDate": datetime.now(),
        "CreatedBy": created_by,
        "Category": category
    }

    df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)

    # ✅ SAVE CLEANLY
    with pd.ExcelWriter(file_path, mode="a", if_sheet_exists="replace", engine="openpyxl") as writer:
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

