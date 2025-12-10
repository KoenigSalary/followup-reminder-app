import pandas as pd
import os
from datetime import datetime
import yaml

from email_engine import send_email

# ✅ Load config safely
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]

# ✅ Owner email (admin copy)
OWNER_EMAIL = os.getenv("TEST_EMAIL") or os.getenv("SMTP_USER")


def process_followups():
    print("✅ Running MoM Follow-up Engine")

    try:
        df = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    except Exception as e:
        print("❌ Could not read Tasks sheet:", e)
        return

    # ✅ Ensure required columns exist
    required_cols = ["Title", "AssignedTo", "Department", "Deadline", "Status"]
    for col in required_cols:
        if col not in df.columns:
            print(f"❌ Missing required column: {col}")
            return

    # ✅ Convert safely
    df["Deadline"] = pd.to_datetime(df["Deadline"], errors="coerce")
    df["Status"] = df["Status"].astype(str).str.lower()

    today = datetime.today().date()
    sent_count = 0

    for _, row in df.iterrows():

        # ✅ Only pending tasks
        if row["Status"] != "pending":
            continue

        # ✅ Skip invalid deadlines
        if pd.isna(row["Deadline"]):
            continue

        due = row["Deadline"].date()

        if today >= due:

            subject = f"⏰ MoM Follow-Up: {row['Title']}"

            body = f"""
Dear {row['AssignedTo']},

This is a reminder for your pending MoM task:

----------------------------------
Task: {row['Title']}
Department: {row['Department']}
Deadline: {due}
----------------------------------

Please update your task status at the earliest.

Regards,
Koenig MoM Automation
"""

            # ✅ Send safely — NO CRASH EVER
            try:
                send_email(row["AssignedTo"], subject, body)

                # ✅ Send admin copy too
                if OWNER_EMAIL:
                    send_email(OWNER_EMAIL, subject, body)

                sent_count += 1

            except Exception as e:
                print("⚠️ Email failed for:", row["Title"], "| Error:", e)

    print(f"✅ Follow-up completed. Emails sent: {sent_count}")
