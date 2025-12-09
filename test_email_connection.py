#!/usr/bin/env python3
"""Test email SMTP and IMAP connection"""

import smtplib
import imaplib
import os
from dotenv import load_dotenv

load_dotenv()

EMAIL_USER = os.getenv('EMAIL_USER')
EMAIL_PASS = os.getenv('EMAIL_PASS') or os.getenv('SMTP_PASS')

print("=" * 60)
print("🧪 Testing Email Connection")
print("=" * 60)
print(f"📧 Email: {EMAIL_USER}")
print(f"🔑 Password: {'*' * len(EMAIL_PASS) if EMAIL_PASS else 'NOT SET'}")
print()

# Test 1: SMTP (Sending)
print("1️⃣ Testing SMTP (Email Sending)...")
try:
    smtp = smtplib.SMTP('smtp.office365.com', 587)
    smtp.starttls()
    smtp.login(EMAIL_USER, EMAIL_PASS)
    smtp.quit()
    print("   ✅ SMTP Connection SUCCESS")
    print("   📤 Email sending is working!")
except Exception as e:
    print(f"   ❌ SMTP Failed: {e}")
    print("   💡 Tip: Check your email password or generate an App Password")

print()

# Test 2: IMAP (Reading)
print("2️⃣ Testing IMAP (Email Reading)...")
try:
    imap = imaplib.IMAP4_SSL('outlook.office365.com')
    imap.login(EMAIL_USER, EMAIL_PASS)
    imap.select('INBOX')
    status, messages = imap.search(None, 'ALL')
    total_emails = len(messages[0].split())
    imap.logout()
    print("   ✅ IMAP Connection SUCCESS")
    print(f"   📬 Total emails in inbox: {total_emails}")
except Exception as e:
    print(f"   ❌ IMAP Failed: {e}")
    print("   💡 Solutions:")
    print("      1. Generate App Password at: https://account.microsoft.com/security")
    print("      2. Enable IMAP in Outlook settings")
    print("      3. Update .env with: EMAIL_PASS=your_app_password")

print()
print("=" * 60)
print("📋 TROUBLESHOOTING GUIDE")
print("=" * 60)
print()
print("If you see 'LOGIN failed' error:")
print()
print("1️⃣ Generate Microsoft App Password:")
print("   → https://account.microsoft.com/security")
print("   → Click 'Advanced security options'")
print("   → Click 'Create a new app password'")
print("   → Copy the password (e.g., 'abcd efgh ijkl mnop')")
print()
print("2️⃣ Update your .env file:")
print("   EMAIL_PASS=abcdefghijklmnop  # Remove spaces!")
print()
print("3️⃣ Enable IMAP in Outlook:")
print("   → https://outlook.office365.com")
print("   → Settings → Mail → Sync email")
print("   → Enable 'Let devices and apps use IMAP'")
print()
print("=" * 60)
