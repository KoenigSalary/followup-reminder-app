# email_engine.py - WITH TEAM EMAIL YAML
import smtplib
import os
import yaml
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from pathlib import Path

# ✅ LOAD ENV EXPLICITLY
load_dotenv(dotenv_path=".env")

# ✅ LOAD TEAM EMAILS FROM YAML
def load_team_emails():
    """Load team email directory from YAML file"""
    try:
        yaml_path = Path("team_emails.yaml")
        if yaml_path.exists():
            with open(yaml_path, 'r') as f:
                data = yaml.safe_load(f)
                return data.get('team_emails', {})
        else:
            print("⚠️  team_emails.yaml not found, using defaults")
            return {}
    except Exception as e:
        print(f"⚠️  Error loading team_emails.yaml: {e}")
        return {}

# Load email directory
EMAIL_DIRECTORY = load_team_emails()

# Add owner as fallback
OWNER_EMAIL = os.getenv("OWNER_EMAIL") or os.getenv("SMTP_USER")
if OWNER_EMAIL:
    EMAIL_DIRECTORY['Owner'] = OWNER_EMAIL
    EMAIL_DIRECTORY['Admin'] = OWNER_EMAIL

def get_email_address(recipient):
    """
    Convert name to email address
    
    Args:
        recipient: Name or email address
    
    Returns:
        str: Email address
    """
    # If it's already an email, return it
    if '@' in str(recipient):
        return recipient
    
    # Remove extra whitespace
    recipient = str(recipient).strip()
    
    # Try exact match first
    if recipient in EMAIL_DIRECTORY:
        return EMAIL_DIRECTORY[recipient]
    
    # Try case-insensitive match
    for name, email in EMAIL_DIRECTORY.items():
        if name.lower() == recipient.lower():
            return email
    
    # Try partial match (first name only)
    first_name = recipient.split()[0] if ' ' in recipient else recipient
    for name, email in EMAIL_DIRECTORY.items():
        if name.lower() == first_name.lower():
            print(f"ℹ️  Matched '{recipient}' → '{name}' → {email}")
            return email
    
    # Default to owner email
    print(f"⚠️  No email found for '{recipient}', using owner: {OWNER_EMAIL}")
    return OWNER_EMAIL


def send_email(to_recipient, subject, body):
    """
    Send email - accepts name or email address
    
    Args:
        to_recipient: Name (e.g. "Sunil") or email
        subject: Email subject
        body: Email body
    
    Returns:
        bool: True if sent, False if failed
    """
    try:
        SMTP_SERVER = os.getenv("SMTP_SERVER")
        SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
        SMTP_USER = os.getenv("SMTP_USER")
        SMTP_PASS = os.getenv("SMTP_PASS")

        if not all([SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASS]):
            raise ValueError("SMTP ENV variables missing")
        
        # ✅ CONVERT NAME TO EMAIL
        to_email = get_email_address(to_recipient)

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

        print(f"✅ Email sent to {to_email} ({to_recipient})")
        return True

    except Exception as e:
        print(f"❌ Email failed to {to_recipient}: {e}")
        import traceback
        traceback.print_exc()
        return False


# ✅ TEST FUNCTION
if __name__ == "__main__":
    print("=" * 70)
    print("🧪 TESTING EMAIL ENGINE WITH TEAM DIRECTORY")
    print("=" * 70)
    
    print(f"\n📋 Loaded {len(EMAIL_DIRECTORY)} email addresses from team_emails.yaml")
    print("\nTeam members:")
    for name, email in list(EMAIL_DIRECTORY.items())[:10]:
        print(f"  • {name}: {email}")
    if len(EMAIL_DIRECTORY) > 10:
        print(f"  ... and {len(EMAIL_DIRECTORY) - 10} more")
    
    # Test lookups
    print("\n🔍 Testing email lookups:")
    test_names = ["Sunil", "Sunil Kumar", "sunilkumar.kushwaha@koenig-solutions.com", "Unknown Person"]
    
    for name in test_names:
        email = get_email_address(name)
        print(f"  '{name}' → {email}")
    
    # Send test email
    print("\n📧 Sending test email...")
    result = send_email(
        to_recipient="Sunil",
        subject="🧪 Test: MoM System Email",
        body="""Dear Team Member,

This is a test email from the Koenig MoM Automation System.

Your email address was successfully resolved from the team directory!

Best regards,
Koenig MoM Automation"""
    )
    
    if result:
        print("\n🎉 SUCCESS! Email engine working with team directory!")
    else:
        print("\n❌ FAILED! Check errors above")
    
    print("=" * 70)
