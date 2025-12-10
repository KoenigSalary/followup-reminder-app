# email_engine.py

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

# ✅ LOAD ENV EXPLICITLY
load_dotenv(dotenv_path=".env")


def send_email(to_email, subject, body):
    try:
        SMTP_SERVER = os.getenv("SMTP_SERVER")
        SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
        SMTP_USER = os.getenv("SMTP_USER")
        SMTP_PASS = os.getenv("SMTP_PASS")

        if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS]):
            raise ValueError("SMTP ENV variables missing")

        msg = MIMEMultipart()
        msg["From"] = SMTP_USER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USER, SMTP_PASS)
        server.send_message(msg)
        server.quit()

        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print("⚠️ Email failed:", e)
