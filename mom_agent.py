# ✅ 4️⃣ CREATE `mom_agent.py` (FOLLOW-UP ENGINE)

~~~python
import pandas as pd
import yaml
from email_engine import send_email
from datetime import date

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]
TEST_EMAIL = config["email"]["test_email"]


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


