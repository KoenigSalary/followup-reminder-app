import pandas as pd
import os
import yaml
import uuid
from datetime import datetime
from dotenv import load_dotenv
from email_engine import send_email

# ✅ Load ENV safely
load_dotenv(dotenv_path=".env")

# ✅ Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]
OWNER_EMAIL = os.getenv("TEST_EMAIL") or os.getenv("SMTP_USER")


def add_task(meeting_id, title, details, department, assigned_to, created_by, deadline, category):

    # ✅ Generate unique Task ID
    task_id = f"TASK-{uuid.uuid4().hex[:8].upper()}"

    # ✅ Fix Meeting ID if AI
    if not meeting_id or meeting_id == "AI-Extract":
        meeting_id = f"AI-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    # ✅ Load file
    df = pd.read_excel(MOM_FILE, sheet_name="Tasks")

    # ✅ Create new row
    new_task = {
        "TaskID": task_id,
        "MeetingID": meeting_id,
        "Title": title,
        "Details": details,
        "Department": department,
        "AssignedTo": assigned_to,
        "Status": "pending",
        "Deadline": deadline,
        "CreatedDate": datetime.now(),
        "CreatedBy": created_by,
        "Category": category
    }

    df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)

    # ✅ Save back
    df.to_excel(MOM_FILE, sheet_name="Tasks", index=False)

    # ✅ Email (Crash-proof)
    subject = f"New MoM Task Assigned: {title}"
    body = f"""
Dear {assigned_to},

You have been assigned a new MoM task.

Task: {title}
Department: {department}
Deadline: {deadline}

Regards,
Praveen Chaudhary
"""

    try:
        send_email(assigned_to, subject, body)
    except Exception as e:
        st.warning("⚠️ User email could not be sent.")
        print("⚠️ User email failed:", e)

    try:
        if OWNER_EMAIL:
            send_email(OWNER_EMAIL, subject, body)
    except Exception as e:
        st.warning("⚠️ Admin email could not be sent.")
        print("⚠️ Admin email failed:", e)

    st.success(f"✅ Task saved successfully: {task_id}")

