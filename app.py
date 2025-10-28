import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import os
from pathlib import Path
import hashlib
import base64

# Email service imports
try:
    from email_service import EmailService
    from email_scheduler import EmailScheduler
    from email_preferences import EmailPreferences
    EMAIL_ENABLED = True
except ImportError:
    EMAIL_ENABLED = False
    print("Email service not available")

# Page config
st.set_page_config(
    page_title="Followup Reminder System",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize data directory
DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
USERS_FILE = DATA_DIR / "users.json"
ITEMS_FILE = DATA_DIR / "followup_items.json"
CONTACTS_FILE = DATA_DIR / "contacts.json"

# Logo path
LOGO_PATH = Path("assets/koenig_logo.png")

# Initialize email service and preferences
if EMAIL_ENABLED:
    email_service = EmailService()
    email_preferences = EmailPreferences()
    # Start background scheduler
    if 'scheduler_started' not in st.session_state:
        email_scheduler = EmailScheduler()
        email_scheduler.run_in_background()
        st.session_state.scheduler_started = True

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'email_notifications' not in st.session_state:
    st.session_state.email_notifications = True

# Helper functions
def load_logo():
    """Load and encode logo for display"""
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

def display_logo():
    """Display Koenig logo in the app"""
    logo_base64 = load_logo()
    if logo_base64:
        st.markdown(
            f"""
            <div style="text-align: center; padding: 10px;">
                <img src="data:image/png;base64,{logo_base64}" alt="Koenig Logo" style="max-width: 200px; height: auto;">
            </div>
            """,
            unsafe_allow_html=True
        )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    if USERS_FILE.exists():
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_contacts():
    """Load external contacts from uploaded list"""
    if CONTACTS_FILE.exists():
        with open(CONTACTS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_contacts(contacts):
    """Save external contacts"""
    with open(CONTACTS_FILE, 'w') as f:
        json.dump(contacts, f, indent=2)

def get_all_usernames():
    """Get list of all registered usernames"""
    users = load_users()
    return sorted(users.keys())

def get_all_contacts():
    """Get combined list of registered users + external contacts"""
    # Registered users
    users = load_users()
    contacts = []
    for username, data in users.items():
        contacts.append({
            'name': username,
            'email': data.get('email'),
            'type': 'registered'
        })
    
    # External contacts
    external = load_contacts()
    for contact in external:
        contacts.append({
            'name': contact['name'],
            'email': contact['email'],
            'type': 'external'
        })
    
    return contacts

def get_contact_names():
    """Get list of all contact names (users + external)"""
    contacts = get_all_contacts()
    return sorted([c['name'] for c in contacts])

def get_contact_email(name):
    """Get email for a contact name"""
    contacts = get_all_contacts()
    for contact in contacts:
        if contact['name'] == name:
            return contact['email']
    return None

def get_user_email(username):
    """Get email for a username (backward compatibility)"""
    return get_contact_email(username)

def load_items():
    if ITEMS_FILE.exists():
        with open(ITEMS_FILE, 'r') as f:
            return json.load(f)
    return []

def save_items(items):
    with open(ITEMS_FILE, 'w') as f:
        json.dump(items, f, indent=2)

def authenticate(username, password):
    users = load_users()
    if username in users and users[username]['password'] == hash_password(password):
        return True
    return False

def register_user(username, password, email):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        'password': hash_password(password),
        'email': email,
        'created_at': datetime.now().isoformat()
    }
    save_users(users)
    return True

# Login/Register Page
def login_page():
    display_logo()
    
    st.title("📋 Followup Reminder System")
    st.markdown("---")
    
    tab1, tab2 = st.tabs(["Login", "Register"])
    
    with tab1:
        st.subheader("Login to Your Account")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", type="primary"):
            if authenticate(username, password):
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid username or password")
    
    with tab2:
        st.subheader("Create New Account")
        new_username = st.text_input("Username", key="reg_username")
        new_email = st.text_input("Email", key="reg_email")
        new_password = st.text_input("Password", type="password", key="reg_password")
        new_password_confirm = st.text_input("Confirm Password", type="password", key="reg_password_confirm")
        
        if st.button("Register", type="primary"):
            if not new_username or not new_password or not new_email:
                st.error("All fields are required")
            elif new_password != new_password_confirm:
                st.error("Passwords do not match")
            elif len(new_password) < 6:
                st.error("Password must be at least 6 characters")
            elif register_user(new_username, new_password, new_email):
                st.success("Account created successfully! Please login.")
            else:
                st.error("Username already exists")

# Main App
def main_app():
    with st.sidebar:
        display_logo()
        st.title(f"👤 {st.session_state.username}")
        st.markdown("---")
        
        if st.button("🚪 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
        
        st.markdown("---")
        st.markdown("### Navigation")
        page = st.radio(
            "Go to",
            ["📊 Dashboard", "➕ Add New Item", "📋 All Items", "🔍 Search & Filter", 
             "📈 Analytics", "📧 Email Settings", "👥 Manage Contacts"],
            label_visibility="collapsed"
        )
    
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "➕ Add New Item":
        add_item_page()
    elif page == "📋 All Items":
        all_items_page()
    elif page == "🔍 Search & Filter":
        search_page()
    elif page == "📈 Analytics":
        analytics_page()
    elif page == "📧 Email Settings":
        email_settings_page()
    elif page == "👥 Manage Contacts":
        manage_contacts_page()

def manage_contacts_page():
    """Manage external contacts who don't have app accounts"""
    st.title("👥 Manage External Contacts")
    st.markdown("---")
    
    st.info("💡 Add team members who don't have app accounts. You can assign tasks to them and they'll receive email notifications.")
    
    # Upload CSV
    st.subheader("📤 Upload Contact List (CSV)")
    st.markdown("**CSV Format:** Name, Email")
    st.code("John Doe, john.doe@company.com\nJane Smith, jane.smith@company.com", language="text")
    
    uploaded_file = st.file_uploader("Upload CSV file", type=['csv'])
    
    if uploaded_file:
        try:
            df = pd.read_csv(uploaded_file)
            
            # Validate columns
            if 'Name' in df.columns and 'Email' in df.columns:
                st.success(f"✅ Found {len(df)} contacts in file")
                st.dataframe(df)
                
                if st.button("Import These Contacts", type="primary"):
                    contacts = load_contacts()
                    imported = 0
                    
                    for _, row in df.iterrows():
                        name = str(row['Name']).strip()
                        email = str(row['Email']).strip()
                        
                        # Check if already exists
                        if not any(c['email'] == email for c in contacts):
                            contacts.append({
                                'name': name,
                                'email': email,
                                'added_by': st.session_state.username,
                                'added_at': datetime.now().isoformat()
                            })
                            imported += 1
                    
                    save_contacts(contacts)
                    st.success(f"✅ Imported {imported} new contacts!")
                    st.balloons()
                    st.rerun()
            else:
                st.error("CSV must have 'Name' and 'Email' columns")
        except Exception as e:
            st.error(f"Error reading CSV: {e}")
    
    st.markdown("---")
    
    # Manual add
    st.subheader("➕ Add Single Contact")
    
    with st.form("add_contact"):
        col1, col2 = st.columns(2)
        
        with col1:
            contact_name = st.text_input("Name*", placeholder="e.g., John Doe")
        
        with col2:
            contact_email = st.text_input("Email*", placeholder="e.g., john.doe@company.com")
        
        if st.form_submit_button("Add Contact", type="primary"):
            if not contact_name or not contact_email:
                st.error("Both fields are required")
            elif '@' not in contact_email:
                st.error("Invalid email format")
            else:
                contacts = load_contacts()
                
                # Check duplicate
                if any(c['email'] == contact_email for c in contacts):
                    st.error("Contact with this email already exists")
                else:
                    contacts.append({
                        'name': contact_name,
                        'email': contact_email,
                        'added_by': st.session_state.username,
                        'added_at': datetime.now().isoformat()
                    })
                    save_contacts(contacts)
                    st.success(f"✅ Added {contact_name}")
                    st.rerun()
    
    st.markdown("---")
    
    # Show all contacts
    st.subheader("📋 All Contacts")
    
    contacts = load_contacts()
    
    if contacts:
        st.write(f"Total external contacts: {len(contacts)}")
        
        # Create dataframe
        contact_data = []
        for contact in contacts:
            contact_data.append({
                'Name': contact['name'],
                'Email': contact['email'],
                'Added By': contact.get('added_by', 'Unknown'),
                'Added At': contact.get('added_at', 'Unknown')[:10]
            })
        
        df = pd.DataFrame(contact_data)
        st.dataframe(df, use_container_width=True)
        
        # Delete contacts
        st.markdown("---")
        st.subheader("🗑️ Delete Contacts")
        
        contact_to_delete = st.selectbox(
            "Select contact to delete",
            options=[c['name'] for c in contacts]
        )
        
        if st.button("Delete Contact", type="secondary"):
            contacts = [c for c in contacts if c['name'] != contact_to_delete]
            save_contacts(contacts)
            st.success(f"✅ Deleted {contact_to_delete}")
            st.rerun()
    else:
        st.info("No external contacts yet. Add some using the form above or upload a CSV.")
    
    # Show registered users
    st.markdown("---")
    st.subheader("👤 Registered Users")
    users = load_users()
    st.write(f"Total registered users: {len(users)}")
    
    user_data = []
    for username, data in users.items():
        user_data.append({
            'Username': username,
            'Email': data.get('email'),
            'Registered': data.get('created_at', 'Unknown')[:10]
        })
    
    if user_data:
        df_users = pd.DataFrame(user_data)
        st.dataframe(df_users, use_container_width=True)

def email_settings_page():
    """Email preferences and settings page"""
    st.title("📧 Email Notification Settings")
    st.markdown("---")
    
    if not EMAIL_ENABLED:
        st.warning("⚠️ Email service is not configured yet. Please contact your administrator.")
        return
    
    st.info("💡 Control which email notifications you receive and manage your preferences.")
    
    prefs = email_preferences.get_user_preferences(st.session_state.username)
    
    st.subheader("🔔 Notification Preferences")
    
    with st.form("email_preferences"):
        email_enabled = st.checkbox(
            "Enable all email notifications",
            value=prefs.get('email_enabled', True),
            help="Turn off to disable all emails"
        )
        
        st.markdown("---")
        st.markdown("### Specific Notification Types")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alternate_digest = st.checkbox(
                "📬 Alternate Day Digest",
                value=prefs.get('alternate_digest', True),
                help="Every 2 days at 8:00 AM - High/Urgent items only",
                disabled=not email_enabled
            )
            
            deadline_alerts = st.checkbox(
                "⚠️ Deadline Alerts",
                value=prefs.get('deadline_alerts', True),
                help="4 days before deadline - checked every 6 hours",
                disabled=not email_enabled
            )
            
            weekly_summary = st.checkbox(
                "📋 Weekly Summary",
                value=prefs.get('weekly_summary', True),
                help="Every Monday at 8:00 AM - all pending items",
                disabled=not email_enabled
            )
        
        with col2:
            status_changes = st.checkbox(
                "🔄 Status Change Notifications",
                value=prefs.get('status_changes', True),
                help="Real-time notifications when item status changes",
                disabled=not email_enabled
            )
            
            completion_celebration = st.checkbox(
                "🎉 Completion Celebrations",
                value=prefs.get('completion_celebration', True),
                help="Celebration emails when items are completed",
                disabled=not email_enabled
            )
        
        st.markdown("---")
        
        if st.form_submit_button("💾 Save Preferences", type="primary"):
            new_prefs = {
                'email_enabled': email_enabled,
                'alternate_digest': alternate_digest,
                'deadline_alerts': deadline_alerts,
                'weekly_summary': weekly_summary,
                'status_changes': status_changes,
                'completion_celebration': completion_celebration
            }
            
            email_preferences.update_user_preferences(st.session_state.username, new_prefs)
            st.success("✅ Email preferences saved successfully!")
    
    st.markdown("---")
    
    st.subheader("📅 Email Schedule Reference")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        **📬 Alternate Digest**
        - Frequency: Every 2 days
        - Time: 8:00 AM
        - Content: High/Urgent priority items only
        """)
    
    with col2:
        st.markdown("""
        **⚠️ Deadline Alerts**
        - Frequency: 4 days before deadline
        - Check: Every 6 hours
        - Content: Items approaching deadline
        """)
    
    with col3:
        st.markdown("""
        **📋 Weekly Summary**
        - Frequency: Every Monday
        - Time: 8:00 AM
        - Content: All pending items
        """)

def dashboard_page():
    st.title("📊 Dashboard")
    st.markdown("---")
    
    items = load_items()
    user_items = [item for item in items if item.get('owner') == st.session_state.username]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total = len(user_items)
        st.metric("Total Items", total)
    
    with col2:
        pending = len([i for i in user_items if i['status'] == 'Pending'])
        st.metric("Pending", pending)
    
    with col3:
        in_progress = len([i for i in user_items if i['status'] == 'In Progress'])
        st.metric("In Progress", in_progress)
    
    with col4:
        completed = len([i for i in user_items if i['status'] == 'Completed'])
        st.metric("Completed", completed)
    
    st.markdown("---")
    
    st.subheader("⏰ Upcoming Deadlines")
    today = datetime.now().date()
    
    upcoming = []
    for item in user_items:
        if item['status'] != 'Completed' and item.get('deadline'):
            deadline = datetime.fromisoformat(item['deadline']).date()
            days_left = (deadline - today).days
            if days_left >= 0:
                item['days_left'] = days_left
                upcoming.append(item)
    
    upcoming.sort(key=lambda x: x['days_left'])
    
    if upcoming:
        for item in upcoming[:5]:
            days = item['days_left']
            if days == 0:
                urgency = "🔴 Due Today!"
            elif days <= 3:
                urgency = f"🟠 {days} days left"
            elif days <= 7:
                urgency = f"🟡 {days} days left"
            else:
                urgency = f"🟢 {days} days left"
            
            with st.expander(f"{urgency} - {item['title']}", expanded=(days <= 3)):
                st.write(f"**Category:** {item['category']}")
                st.write(f"**Priority:** {item['priority']}")
                st.write(f"**Responsible:** {item['responsible']}")
                st.write(f"**Description:** {item['description']}")
                
                if EMAIL_ENABLED and item.get('send_to_responsible'):
                    st.info(f"📧 Reminders will be sent to: {item.get('responsible', 'Not specified')}")
    else:
        st.info("No upcoming deadlines")
    
    st.markdown("---")
    
    st.subheader("📌 Recent Items")
    recent = sorted(user_items, key=lambda x: x['created_at'], reverse=True)[:5]
    
    if recent:
        for item in recent:
            status_emoji = {"Pending": "⏳", "In Progress": "🔄", "Completed": "✅", "Blocked": "🚫"}
            st.write(f"{status_emoji[item['status']]} **{item['title']}** - {item['category']} ({item['priority']})")
    else:
        st.info("No items yet")

def add_item_page():
    st.title("➕ Add New Followup Item")
    st.markdown("---")
    
    input_method = st.radio(
        "Choose input method:",
        ["Quick Entry Form", "Paste MOM Text", "Upload Document", "AI Extract from Text"],
        horizontal=True
    )
    
    if input_method == "Quick Entry Form":
        quick_entry_form()
    elif input_method == "Paste MOM Text":
        paste_mom_text()
    elif input_method == "Upload Document":
        upload_document()
    elif input_method == "AI Extract from Text":
        ai_extract_form()

def quick_entry_form():
    st.subheader("Quick Entry Form")
    
    all_contacts = get_contact_names()
    
    with st.form("quick_entry"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title/Action Item*", placeholder="e.g., Prepare Q4 report")
            category = st.selectbox("Category", ["Team Meeting", "Boss Meeting", "Personal Note", "Project", "Other"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
            
            responsible = st.selectbox(
                "Person Responsible*",
                options=all_contacts,
                help="Select who will be responsible for this task (includes registered users + external contacts)"
            )
        
        with col2:
            deadline = st.date_input("Deadline", min_value=datetime.now().date())
            reminder_days = st.number_input("Remind me (days before deadline)", min_value=0, value=3)
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "Blocked"])
            tags = st.text_input("Tags (comma separated)", placeholder="e.g., urgent, finance, review")
        
        description = st.text_area("Description/Notes", placeholder="Add detailed notes here...")
        
        if EMAIL_ENABLED:
            st.markdown("---")
            st.markdown("### 📧 Email Notification Settings")
            
            col3, col4 = st.columns(2)
            
            with col3:
                send_to_responsible = st.checkbox(
                    "Send reminders to Responsible person",
                    value=True,
                    help="Email notifications will go to the person responsible for this task"
                )
                
                cc_owner = st.checkbox(
                    "CC me (Owner) on all emails",
                    value=True,
                    help="You'll receive a copy of all emails for this item"
                )
            
            with col4:
                additional_recipients = st.multiselect(
                    "Also notify (optional):",
                    options=[c for c in all_contacts if c != responsible and c != st.session_state.username],
                    help="Select additional people to receive notifications"
                )
            
            recipients_list = []
            if send_to_responsible:
                recipients_list.append(f"**{responsible}** (Responsible)")
            if cc_owner:
                recipients_list.append(f"**{st.session_state.username}** (Owner - CC)")
            if additional_recipients:
                recipients_list.extend([f"**{r}** (Additional)" for r in additional_recipients])
            
            if recipients_list:
                st.info("📨 Email notifications will be sent to: " + ", ".join(recipients_list))
            else:
                st.warning("⚠️ No email recipients selected!")
        
        submitted = st.form_submit_button("Add Item", type="primary")
        
        if submitted:
            if not title:
                st.error("Title is required")
            elif not responsible:
                st.error("Please select a person responsible")
            else:
                items = load_items()
                
                responsible_email = get_contact_email(responsible)
                owner_email = get_contact_email(st.session_state.username)
                additional_emails = [get_contact_email(u) for u in additional_recipients] if additional_recipients else []
                
                new_item = {
                    'id': len(items) + 1,
                    'title': title,
                    'description': description,
                    'category': category,
                    'priority': priority,
                    'responsible': responsible,
                    'responsible_email': responsible_email,
                    'deadline': deadline.isoformat(),
                    'reminder_days': reminder_days,
                    'status': status,
                    'tags': [t.strip() for t in tags.split(',') if t.strip()],
                    'owner': st.session_state.username,
                    'owner_email': owner_email,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat(),
                    'send_to_responsible': send_to_responsible if EMAIL_ENABLED else False,
                    'cc_owner': cc_owner if EMAIL_ENABLED else False,
                    'additional_recipients': additional_emails if EMAIL_ENABLED else []
                }
                items.append(new_item)
                save_items(items)
                st.success("✅ Item added successfully!")
                
                if EMAIL_ENABLED and (send_to_responsible or cc_owner or additional_emails):
                    st.success(f"📧 Email notifications configured for {len(recipients_list)} recipient(s)")
                
                st.balloons()

def paste_mom_text():
    st.subheader("Paste Minutes of Meeting")
    st.info("Paste your MOM text below and AI will extract action items automatically")
    
    mom_text = st.text_area("Paste MOM here", height=300, placeholder="Paste your meeting minutes here...")
    
    if st.button("Extract Action Items", type="primary"):
        if mom_text:
            lines = mom_text.split('\n')
            action_items = []
            
            for line in lines:
                line = line.strip()
                if any(keyword in line.lower() for keyword in ['action:', 'todo:', 'task:', 'followup:', 'follow-up:', '-']):
                    if len(line) > 5:
                        action_items.append(line)
            
            if action_items:
                st.success(f"Found {len(action_items)} potential action items!")
                st.subheader("Review and Add Items:")
                
                all_contacts = get_contact_names()
                
                for idx, item in enumerate(action_items):
                    with st.expander(f"Action Item {idx+1}: {item[:50]}...", expanded=True):
                        with st.form(f"extracted_item_{idx}"):
                            title = st.text_input("Title", value=item)
                            col1, col2 = st.columns(2)
                            with col1:
                                category = st.selectbox("Category", ["Team Meeting", "Boss Meeting", "Personal Note", "Project"], key=f"cat_{idx}")
                                priority = st.selectbox("Priority", ["Medium", "Low", "High", "Urgent"], key=f"pri_{idx}")
                            with col2:
                                deadline = st.date_input("Deadline", min_value=datetime.now().date(), key=f"dead_{idx}")
                                responsible = st.selectbox("Responsible", all_contacts, key=f"resp_{idx}")
                            
                            if EMAIL_ENABLED:
                                col3, col4 = st.columns(2)
                                with col3:
                                    send_to_responsible = st.checkbox("Send to Responsible", value=True, key=f"send_{idx}")
                                with col4:
                                    cc_owner = st.checkbox("CC me", value=True, key=f"cc_{idx}")
                            
                            if st.form_submit_button("Add This Item"):
                                items = load_items()
                                
                                responsible_email = get_contact_email(responsible)
                                owner_email = get_contact_email(st.session_state.username)
                                
                                new_item = {
                                    'id': len(items) + 1,
                                    'title': title,
                                    'description': mom_text[:500],
                                    'category': category,
                                    'priority': priority,
                                    'responsible': responsible,
                                    'responsible_email': responsible_email,
                                    'deadline': deadline.isoformat(),
                                    'reminder_days': 3,
                                    'status': 'Pending',
                                    'tags': ['mom', 'extracted'],
                                    'owner': st.session_state.username,
                                    'owner_email': owner_email,
                                    'created_at': datetime.now().isoformat(),
                                    'updated_at': datetime.now().isoformat(),
                                    'send_to_responsible': send_to_responsible if EMAIL_ENABLED else False,
                                    'cc_owner': cc_owner if EMAIL_ENABLED else False,
                                    'additional_recipients': []
                                }
                                items.append(new_item)
                                save_items(items)
                                st.success("✅ Item added!")
            else:
                st.warning("No action items found. Try using keywords like 'Action:', 'TODO:', or bullet points.")
        else:
            st.error("Please paste some text first")

def upload_document():
    st.subheader("Upload Document")
    st.info("Upload PDF, Word, or text files containing meeting minutes")
    
    uploaded_file = st.file_uploader("Choose a file", type=['pdf', 'docx', 'txt', 'doc'])
    
    if uploaded_file:
        st.success(f"File uploaded: {uploaded_file.name}")
        st.info("Document processing feature coming soon! For now, please copy the text and use 'Paste MOM Text' option.")

def ai_extract_form():
    st.subheader("AI Extract from Free Text")
    st.info("Enter any text and AI will identify action items, deadlines, and responsibilities")
    
    free_text = st.text_area("Enter text", height=200, placeholder="Type or paste any text containing action items...")
    
    if st.button("AI Extract", type="primary"):
        if free_text:
            st.info("AI extraction feature uses advanced NLP. For now, using keyword-based extraction.")
            st.success("Processing... This feature will be enhanced with OpenAI/Gemini integration")
        else:
            st.error("Please enter some text")


def all_items_page():
    st.title("📋 All Followup Items")
    st.markdown("---")
    
    items = load_items()
    user_items = [item for item in items if item.get('owner') == st.session_state.username]
    
    if not user_items:
        st.info("No items yet. Add your first followup item!")
        return
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_status = st.multiselect("Filter by Status", ["Pending", "In Progress", "Completed", "Blocked"], default=["Pending", "In Progress"])
    
    with col2:
        filter_priority = st.multiselect("Filter by Priority", ["Low", "Medium", "High", "Urgent"])
    
    with col3:
        filter_category = st.multiselect("Filter by Category", list(set([i['category'] for i in user_items])))
    
    filtered_items = user_items
    
    if filter_status:
        filtered_items = [i for i in filtered_items if i['status'] in filter_status]
    
    if filter_priority:
        filtered_items = [i for i in filtered_items if i['priority'] in filter_priority]
    
    if filter_category:
        filtered_items = [i for i in filtered_items if i['category'] in filter_category]
    
    st.write(f"Showing {len(filtered_items)} items")
    st.markdown("---")
    
    for item in sorted(filtered_items, key=lambda x: x.get('deadline', '9999-99-99')):
        with st.expander(f"{item['priority']} - {item['title']} ({item['status']})", expanded=False):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**Description:** {item['description']}")
                st.write(f"**Category:** {item['category']}")
                st.write(f"**Responsible:** {item['responsible']}")
                st.write(f"**Deadline:** {item.get('deadline', 'Not set')}")
                st.write(f"**Tags:** {', '.join(item.get('tags', []))}")
                st.write(f"**Created:** {item['created_at'][:10]}")
                
                if EMAIL_ENABLED:
                    email_info = []
                    if item.get('send_to_responsible'):
                        email_info.append(f"→ {item['responsible']}")
                    if item.get('cc_owner'):
                        email_info.append(f"CC: {item['owner']}")
                    if item.get('additional_recipients'):
                        email_info.append(f"Also: {len(item['additional_recipients'])} others")
                    
                    if email_info:
                        st.write(f"**📧 Notifications:** {' | '.join(email_info)}")
            
            with col2:
                new_status = st.selectbox("Update Status", ["Pending", "In Progress", "Completed", "Blocked"], 
                                         index=["Pending", "In Progress", "Completed", "Blocked"].index(item['status']),
                                         key=f"status_{item['id']}")
                
                if st.button("Update", key=f"update_{item['id']}"):
                    items = load_items()
                    for i in items:
                        if i['id'] == item['id']:
                            i['status'] = new_status
                            i['updated_at'] = datetime.now().isoformat()
                    save_items(items)
                    st.success("Updated!")
                    st.rerun()
                
                if st.button("Delete", key=f"delete_{item['id']}", type="secondary"):
                    items = load_items()
                    items = [i for i in items if i['id'] != item['id']]
                    save_items(items)
                    st.success("Deleted!")
                    st.rerun()

def search_page():
    st.title("🔍 Search & Filter")
    st.markdown("---")
    
    search_query = st.text_input("🔎 Search in titles and descriptions", placeholder="Type to search...")
    
    items = load_items()
    user_items = [item for item in items if item.get('owner') == st.session_state.username]
    
    if search_query:
        results = []
        for item in user_items:
            if (search_query.lower() in item['title'].lower() or 
                search_query.lower() in item['description'].lower()):
                results.append(item)
        
        st.write(f"Found {len(results)} results for '{search_query}'")
        
        for item in results:
            with st.expander(f"{item['title']} - {item['category']}", expanded=True):
                st.write(f"**Status:** {item['status']}")
                st.write(f"**Priority:** {item['priority']}")
                st.write(f"**Responsible:** {item['responsible']}")
                st.write(f"**Description:** {item['description']}")
                st.write(f"**Deadline:** {item.get('deadline', 'Not set')}")
    else:
        st.info("Enter a search term to find items")

def analytics_page():
    st.title("📈 Analytics & Insights")
    st.markdown("---")
    
    items = load_items()
    user_items = [item for item in items if item.get('owner') == st.session_state.username]
    
    if not user_items:
        st.info("No data to analyze yet")
        return
    
    total = len(user_items)
    completed = len([i for i in user_items if i['status'] == 'Completed'])
    completion_rate = (completed / total * 100) if total > 0 else 0
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    with col2:
        overdue = len([i for i in user_items if i.get('deadline') and 
                      datetime.fromisoformat(i['deadline']).date() < datetime.now().date() 
                      and i['status'] != 'Completed'])
        st.metric("Overdue Items", overdue)
    
    with col3:
        avg_completion = "N/A"
        st.metric("Avg. Completion Time", avg_completion)
    
    st.markdown("---")
    
    st.subheader("Status Distribution")
    status_counts = {}
    for item in user_items:
        status = item['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    st.bar_chart(status_counts)
    
    st.markdown("---")
    
    st.subheader("Priority Distribution")
    priority_counts = {}
    for item in user_items:
        priority = item['priority']
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    st.bar_chart(priority_counts)
    
    st.markdown("---")
    
    st.subheader("Category Breakdown")
    category_counts = {}
    for item in user_items:
        category = item['category']
        category_counts[category] = category_counts.get(category, 0) + 1
    
    st.bar_chart(category_counts)

# Main execution
if not st.session_state.logged_in:
    login_page()
else:
    main_app()
