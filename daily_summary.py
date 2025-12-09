import pandas as pd
import os
import yaml
from datetime import datetime
from email_engine import send_email

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

MOM_FILE = config["paths"]["mom_file"]
OWNER_EMAIL = os.getenv("TEST_EMAIL")

def send_daily_summary():
    df = pd.read_excel(MOM_FILE, sheet_name="Tasks")

    total = len(df)
    pending = len(df[df["Status"] == "pending"])
    completed = len(df[df["Status"] == "completed"])
    overdue = len(df[(df["Status"] == "pending") & (pd.to_datetime(df["Deadline"]) < datetime.today())])

    today = datetime.today().strftime("%Y-%m-%d")

    body = f"""
📊 DAILY MoM SUMMARY – {today}

✅ Completed: {completed}
⏳ Pending: {pending}
🔥 Overdue: {overdue}
"""

    send_email(
        OWNER_EMAIL,
        f"Daily MoM Summary – {today}",
        body
    )

    print("✅ Daily summary email sent")

if __name__ == "__main__":
    send_daily_summary()
