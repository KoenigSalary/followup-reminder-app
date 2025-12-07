import pandas as pd
from datetime import date, timedelta
import os
import yaml

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]

# ========================================================
# SAMPLE DATA GENERATOR
# ========================================================

def generate_sample_excel():
    print("Creating sample MoM Excel file with test data...")

    # ----------------------------------------------------
    # USERS SHEET
    # ----------------------------------------------------
    users = pd.DataFrame([
        {
            "UserID": 1,
            "Name": "Praveen Chaudhary",
            "Email": "praveen.chaudhary@koenig-solutions.com",
            "Department": "EA-Director’s Office",
            "Role": "Manager"
        },
        {
            "UserID": 2,
            "Name": "Amit Kumar",
            "Email": "praveen.chaudhary@koenig-solutions.com",
            "Department": "Accounts/Finance",
            "Role": "Executive"
        },
        {
            "UserID": 3,
            "Name": "Rohit Sharma",
            "Email": "praveen.chaudhary@koenig-solutions.com",
            "Department": "Sales",
            "Role": "Executive"
        },
        {
            "UserID": 4,
            "Name": "RMS Team Member",
            "Email": "praveen.chaudhary@koenig-solutions.com",
            "Department": "RMS Team",
            "Role": "Executive"
        }
    ])

    # ----------------------------------------------------
    # TASKS SHEET
    # ----------------------------------------------------
    today = date.today()
    deadline1 = today + timedelta(days=3)
    deadline2 = today - timedelta(days=2)  # overdue

    tasks = pd.DataFrame([
        {
            "TaskID": 1,
            "MeetingID": 100,
            "Title": "Submit monthly report",
            "Details": "Prepare and submit monthly analytics report",
            "Department": "Accounts/Finance",
            "AssignedTo": 2,
            "CreatedBy": 1,
            "CreatedDate": today,
            "Deadline": deadline1,
            "Status": "pending",
            "LastUpdateDate": "",
            "LastUpdateBy": ""
        },
        {
            "TaskID": 2,
            "MeetingID": 999,  # Boss MoM
            "Title": "Share latest sales forecast",
            "Details": "Provide updated revenue forecast for next quarter",
            "Department": "Sales",
            "AssignedTo": 3,
            "CreatedBy": 1,
            "CreatedDate": today,
            "Deadline": deadline2,
            "Status": "pending",
            "LastUpdateDate": "",
            "LastUpdateBy": ""
        }
    ])

    # ----------------------------------------------------
    # MEETINGS SHEET
    # ----------------------------------------------------
    meetings = pd.DataFrame([
        {"MeetingID": 100, "MeetingName": "Weekly Finance Review", "Date": today},
        {"MeetingID": 999, "MeetingName": "Boss – Strategic Review", "Date": today},
    ])

    # ----------------------------------------------------
    # LOGS SHEET
    # ----------------------------------------------------
    logs = pd.DataFrame([
        {"LogID": 1, "TaskID": 1, "Action": "created", "Timestamp": today, "Actor": 1},
        {"LogID": 2, "TaskID": 2, "Action": "created", "Timestamp": today, "Actor": 1},
    ])

    # ----------------------------------------------------
    # ESCALATIONS SHEET
    # ----------------------------------------------------
    esc = pd.DataFrame([
        {"EscalationID": 1, "TaskID": 2, "Level": 1, "Date": today, "EscalatedTo": 1}
    ])

    # ----------------------------------------------------
    # SAVE TO EXCEL
    # ----------------------------------------------------
    os.makedirs(os.path.dirname(MOM_FILE), exist_ok=True)

    with pd.ExcelWriter(MOM_FILE, engine="openpyxl") as writer:
        users.to_excel(writer, sheet_name="Users", index=False)
        tasks.to_excel(writer, sheet_name="Tasks", index=False)
        meetings.to_excel(writer, sheet_name="Meetings", index=False)
        logs.to_excel(writer, sheet_name="Logs", index=False)
        esc.to_excel(writer, sheet_name="Escalations", index=False)

    print(f"Sample data created successfully at:\n{MOM_FILE}")


if __name__ == "__main__":
    generate_sample_excel()