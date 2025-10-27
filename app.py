import streamlit as st
import pandas as pd
import json
from datetime import datetime, timedelta
import os
from pathlib import Path
import hashlib
import base64

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

# Logo path
LOGO_PATH = Path("assets/koenig_logo.png")

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

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
    # Display logo
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
    # Sidebar
    with st.sidebar:
        # Display logo in sidebar
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
            ["📊 Dashboard", "➕ Add New Item", "📋 All Items", "🔍 Search & Filter", "📈 Analytics"],
            label_visibility="collapsed"
        )
    
    # Main content
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

def dashboard_page():
    st.title("📊 Dashboard")
    st.markdown("---")
    
    items = load_items()
    user_items = [item for item in items if item.get('owner') == st.session_state.username]
    
    # Stats
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
    
    # Upcoming deadlines
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
        for item in upcoming[:5]:  # Show top 5
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
    else:
        st.info("No upcoming deadlines")
    
    st.markdown("---")
    
    # Recent items
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
    
    # Input method selection
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
    
    with st.form("quick_entry"):
        col1, col2 = st.columns(2)
        
        with col1:
            title = st.text_input("Title/Action Item*", placeholder="e.g., Prepare Q4 report")
            category = st.selectbox("Category", ["Team Meeting", "Boss Meeting", "Personal Note", "Project", "Other"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
            responsible = st.text_input("Person Responsible", placeholder="e.g., John Doe")
        
        with col2:
            deadline = st.date_input("Deadline", min_value=datetime.now().date())
            reminder_days = st.number_input("Remind me (days before deadline)", min_value=0, value=3)
            status = st.selectbox("Status", ["Pending", "In Progress", "Completed", "Blocked"])
            tags = st.text_input("Tags (comma separated)", placeholder="e.g., urgent, finance, review")
        
        description = st.text_area("Description/Notes", placeholder="Add detailed notes here...")
        
        submitted = st.form_submit_button("Add Item", type="primary")
        
        if submitted:
            if not title:
                st.error("Title is required")
            else:
                items = load_items()
                new_item = {
                    'id': len(items) + 1,
                    'title': title,
                    'description': description,
                    'category': category,
                    'priority': priority,
                    'responsible': responsible,
                    'deadline': deadline.isoformat(),
                    'reminder_days': reminder_days,
                    'status': status,
                    'tags': [t.strip() for t in tags.split(',') if t.strip()],
                    'owner': st.session_state.username,
                    'created_at': datetime.now().isoformat(),
                    'updated_at': datetime.now().isoformat()
                }
                items.append(new_item)
                save_items(items)
                st.success("✅ Item added successfully!")
                st.balloons()

def paste_mom_text():
    st.subheader("Paste Minutes of Meeting")
    st.info("Paste your MOM text below and AI will extract action items automatically")
    
    mom_text = st.text_area("Paste MOM here", height=300, placeholder="Paste your meeting minutes here...")
    
    if st.button("Extract Action Items", type="primary"):
        if mom_text:
            # Simple extraction logic (can be enhanced with actual AI)
            lines = mom_text.split('\n')
            action_items = []
            
            for line in lines:
                line = line.strip()
                # Look for action indicators
                if any(keyword in line.lower() for keyword in ['action:', 'todo:', 'task:', 'followup:', 'follow-up:', '-']):
                    if len(line) > 5:
                        action_items.append(line)
            
            if action_items:
                st.success(f"Found {len(action_items)} potential action items!")
                st.subheader("Review and Add Items:")
                
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
                                responsible = st.text_input("Responsible", key=f"resp_{idx}")
                            
                            if st.form_submit_button("Add This Item"):
                                items = load_items()
                                new_item = {
                                    'id': len(items) + 1,
                                    'title': title,
                                    'description': mom_text[:500],
                                    'category': category,
                                    'priority': priority,
                                    'responsible': responsible,
                                    'deadline': deadline.isoformat(),
                                    'reminder_days': 3,
                                    'status': 'Pending',
                                    'tags': ['mom', 'extracted'],
                                    'owner': st.session_state.username,
                                    'created_at': datetime.now().isoformat(),
                                    'updated_at': datetime.now().isoformat()
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
            # Similar to paste_mom_text logic
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
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filter_status = st.multiselect("Filter by Status", ["Pending", "In Progress", "Completed", "Blocked"], default=["Pending", "In Progress"])
    
    with col2:
        filter_priority = st.multiselect("Filter by Priority", ["Low", "Medium", "High", "Urgent"])
    
    with col3:
        filter_category = st.multiselect("Filter by Category", list(set([i['category'] for i in user_items])))
    
    # Apply filters
    filtered_items = user_items
    
    if filter_status:
        filtered_items = [i for i in filtered_items if i['status'] in filter_status]
    
    if filter_priority:
        filtered_items = [i for i in filtered_items if i['priority'] in filter_priority]
    
    if filter_category:
        filtered_items = [i for i in filtered_items if i['category'] in filter_category]
    
    st.write(f"Showing {len(filtered_items)} items")
    st.markdown("---")
    
    # Display items
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
    
    # Completion rate
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
    
    # Status distribution
    st.subheader("Status Distribution")
    status_counts = {}
    for item in user_items:
        status = item['status']
        status_counts[status] = status_counts.get(status, 0) + 1
    
    st.bar_chart(status_counts)
    
    st.markdown("---")
    
    # Priority distribution
    st.subheader("Priority Distribution")
    priority_counts = {}
    for item in user_items:
        priority = item['priority']
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    st.bar_chart(priority_counts)
    
    st.markdown("---")
    
    # Category breakdown
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
