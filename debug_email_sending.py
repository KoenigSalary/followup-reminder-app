#!/usr/bin/env python3
"""
Debug why emails don't send after task creation
"""

import os
from pathlib import Path

print("=" * 70)
print("🔍 DEBUGGING EMAIL SENDING IN add_task()")
print("=" * 70)

# Check 1: Does email_engine.py exist?
print("\n1️⃣ Check email_engine.py exists:")
if Path("email_engine.py").exists():
    print("   ✅ email_engine.py found")
else:
    print("   ❌ email_engine.py NOT FOUND!")
    print("   → This is the problem! Download email_engine.py")

# Check 2: Does team_emails.yaml exist?
print("\n2️⃣ Check team_emails.yaml exists:")
if Path("team_emails.yaml").exists():
    print("   ✅ team_emails.yaml found")
else:
    print("   ⚠️  team_emails.yaml NOT FOUND")
    print("   → Emails will use fallback (owner email)")

# Check 3: Can we import send_email?
print("\n3️⃣ Try importing send_email:")
try:
    from email_engine import send_email
    print("   ✅ send_email imported successfully")
except ImportError as e:
    print(f"   ❌ Import failed: {e}")
    print("   → email_engine.py has errors or is missing")

# Check 4: Check SMTP credentials
print("\n4️⃣ Check SMTP credentials in environment:")
from dotenv import load_dotenv
load_dotenv()

smtp_user = os.getenv('SMTP_USER')
smtp_pass = os.getenv('SMTP_PASS')
smtp_server = os.getenv('SMTP_SERVER')
smtp_port = os.getenv('SMTP_PORT')

print(f"   SMTP_SERVER: {smtp_server or '❌ NOT SET'}")
print(f"   SMTP_PORT: {smtp_port or '❌ NOT SET'}")
print(f"   SMTP_USER: {smtp_user or '❌ NOT SET'}")
print(f"   SMTP_PASS: {'✅ SET (' + smtp_pass[-4:] + ')' if smtp_pass else '❌ NOT SET'}")

# Check 5: Test send_email function
print("\n5️⃣ Test send_email() function:")
try:
    from email_engine import send_email
    
    result = send_email(
        to_recipient="Test User",
        subject="🧪 Debug Test Email",
        body="This is a test to check if email sending works"
    )
    
    if result:
        print("   ✅ Email sent successfully!")
    else:
        print("   ❌ Email function returned False")
        
except Exception as e:
    print(f"   ❌ Email test failed: {e}")
    import traceback
    traceback.print_exc()

# Check 6: Look at mom_agent.py email code
print("\n6️⃣ Check mom_agent.py email sending code:")
mom_path = Path("mom_agent.py")
if mom_path.exists():
    content = mom_path.read_text()
    
    if "from email_engine import send_email" in content:
        print("   ✅ Imports send_email from email_engine")
    else:
        print("   ❌ Does NOT import send_email!")
        print("   → Add: from email_engine import send_email")
    
    if "send_email(" in content:
        print("   ✅ Calls send_email() function")
        
        # Count how many times
        count = content.count("send_email(")
        print(f"   → Called {count} time(s) in the file")
    else:
        print("   ❌ Never calls send_email()!")
        print("   → Email code exists but is never executed")
    
    # Check if it's in try/except that swallows errors
    if "except Exception as e:" in content and "send_email" in content:
        print("   ⚠️  Email is in try/except block")
        print("   → Errors might be silently caught")
        print("   → Check console output for '⚠️ User email failed'")

print("\n" + "=" * 70)
print("🎯 DIAGNOSIS COMPLETE")
print("=" * 70)
print("\n💡 Next steps:")
print("1. If any ❌ above, fix those first")
print("2. Check Streamlit console for '⚠️ User email failed' messages")
print("3. If no errors shown, email code might not be running at all")
print("=" * 70)
