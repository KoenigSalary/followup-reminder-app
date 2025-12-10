#!/usr/bin/env python3
"""
Koenig MoM Automation Dashboard - FIXED VERSION
✅ Handles missing Category column
✅ All 10 tabs
✅ All features working
"""

import streamlit as st
import pandas as pd
import os
import yaml
from datetime import datetime, timedelta
from dotenv import load_dotenv
from openai import OpenAI
import json

# Load environment variables
load_dotenv()

# Import custom modules
from mom_agent import add_task, send_email
from email_reply_processor import process_inbox_replies

# ============= CONFIGURATION =============
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

MOM_FILE = config['paths']['mom_file']
LOGO_PATH = config['branding'].get('logo_url', '')

# ============= PAGE CONFIG =============
st.set_page_config(
    page_title="Koenig MoM Automation Dashboard",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============= CUSTOM CSS =============
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E3A8A;
        font-weight: 700;
        text-align: center;
        padding: 1rem 0;
        border-bottom: 3px solid #DC2626;
    }
    .metric-card {
        background: linear-gradient(135deg, #1E3A8A 0%, #3B82F6 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .overdue-card {
        background: linear-gradient(135deg, #DC2626 0%, #EF4444 100%);
    }
    .stButton > button {
        width: 100%;
        background: #1E3A8A;
        color: white;
        font-weight: 600;
        border-radius: 8px;
        padding: 0.75rem;
        transition: all 0.3s;
    }
    .stButton > button:hover {
        background: #DC2626;
        transform: translateY(-2px);
    }
</style>
""", unsafe_allow_html=True)

# ============= LOAD DATA =============
@st.cache_data(ttl=60)
def load_data():
    """Load all data from Excel"""
    try:
        users = pd.read_excel(MOM_FILE, sheet_name='Users')
        tasks = pd.read_excel(MOM_FILE, sheet_name='Tasks')
        meetings = pd.read_excel(MOM_FILE, sheet_name='Meetings')
        logs = pd.read_excel(MOM_FILE, sheet_name='Logs')
        escalations = pd.read_excel(MOM_FILE, sheet_name='Escalations')
        # FIX: Add Category column if missing
        if 'Category' not in tasks.columns:
            tasks['Category'] = 'Regular'
        
        # FIX: Add Category column if missing
        if 'Category' not in tasks.columns:
            tasks['Category'] = 'Regular'
        
        # Convert dates
        if 'LastUpdateDate' in tasks.columns:
            tasks['LastUpdateDate'] = pd.to_datetime(tasks['LastUpdateDate'], errors='coerce')
        if 'Deadline' in tasks.columns:
            tasks['Deadline'] = pd.to_datetime(tasks['Deadline'], errors='coerce')
        if 'CreatedDate' in tasks.columns:
            tasks['CreatedDate'] = pd.to_datetime(tasks['CreatedDate'], errors='coerce')
        
        return users, tasks, meetings, logs, escalations
    except FileNotFoundError:
        st.error(f"❌ MoM_Master.xlsx not found at: {MOM_FILE}")
        st.stop()

users, tasks, meetings, logs, escalations = load_data()

# ============= HEADER =============
st.markdown(f'<h1 class="main-header">📋 {config["branding"]["dashboard_title"]}</h1>', unsafe_allow_html=True)

# ============= SIDEBAR =============
with st.sidebar:
    if LOGO_PATH:
        try:
            st.image(LOGO_PATH, width=200)
        except:
            st.markdown("### 📋 Koenig MoM")
    
    st.markdown("### 🎛️ Dashboard Controls")
    
    # Refresh Data Button
    if st.button("🔄 Refresh Data", key="refresh_data"):
        st.cache_data.clear()
        st.rerun()
    
    st.markdown("---")
    
    # Status Summary
    st.markdown("### 📊 Quick Stats")
    total_tasks = len(tasks)
    pending_tasks = len(tasks[tasks['Status'] == 'pending'])
    completed_tasks = len(tasks[tasks['Status'] == 'completed'])
    
    st.metric("Total Tasks", total_tasks)
    st.metric("Pending", pending_tasks)
    st.metric("Completed", completed_tasks)
    
    st.markdown("---")
    
    # ============= ADMIN CONTROLS =============
    st.markdown("### ⚙️ Admin Controls")
    
    # REFRESH/RESET BUTTON
    st.markdown("#### 🧹 Reset Testing Data")
    if st.button("🗑️ Clear All Testing Data", key="reset_testing"):
        try:
            df = pd.read_excel(MOM_FILE, sheet_name='Tasks')
            testing_count = len(df[df['Status'] == 'testing'])
            
            if testing_count > 0:
                df_clean = df[df['Status'] != 'testing'].copy()
                with pd.ExcelWriter(MOM_FILE, mode='a', if_sheet_exists='overlay', engine='openpyxl') as writer:
                    df_clean.to_excel(writer, sheet_name='Tasks', index=False)
                st.success(f"✅ Deleted {testing_count} testing task(s)")
                st.cache_data.clear()
                st.rerun()
            else:
                st.info("ℹ️ No testing data found")
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    st.markdown("---")
    
    # MANUAL EMAIL SEND
    st.markdown("#### 📧 Manual Email Test")
    test_recipient = st.text_input("Recipient Email", value=os.getenv('TEST_EMAIL', ''))
    test_subject = st.text_input("Subject", value="Chennai RRF")
    test_body = st.text_area("Body", value="Dear COM, I have shared Chennai RRF with you, Kindly Acknowledge✅")
    
    if st.button("📤 Send Test Email", key="send_test_email"):
        if test_recipient and test_subject and test_body:
            try:
                send_email(test_recipient, test_subject, test_body)
                st.success(f"✅ Email sent to {test_recipient}")
            except Exception as e:
                st.error(f"❌ Error: {e}")
        else:
            st.warning("⚠️ Please fill all fields")
    
    st.markdown("---")
    
    # EMAIL REPLY PROCESSOR
    st.markdown("#### 📬 Process Inbox Replies")
    if st.button("📥 Check & Process Emails", key="process_inbox"):
        with st.spinner("🔍 Reading inbox..."):
            try:
                process_inbox_replies()
                st.success("✅ Inbox processed successfully")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error: {e}")

# ============= MAIN TABS =============
tabs = st.tabs([
    "📊 Dashboard",
    "📝 All Tasks",
    "👔 Boss-MoM",
    "🏢 Departments",
    "➕ Add Task",
    "⚠️ Escalations",
    "🤖 AI MoM Extractor",
    "👤 Executive",
    "👨‍💼 Manager",
    "📈 Performance"
])

# ============= TAB 1: DASHBOARD =============
with tabs[0]:
    st.markdown("### 📊 Overview Summary")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Total Tasks", len(tasks))
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        pending = len(tasks[tasks['Status'] == 'pending'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Pending", pending)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col3:
        completed = len(tasks[tasks['Status'] == 'completed'])
        st.markdown('<div class="metric-card">', unsafe_allow_html=True)
        st.metric("Completed", completed)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col4:
        today = pd.Timestamp.now().normalize()
        overdue = len(tasks[(tasks['Status'] == 'pending') & (tasks['Deadline'] < today)])
        st.markdown('<div class="metric-card overdue-card">', unsafe_allow_html=True)
        st.metric("Overdue", overdue)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Recent Tasks
    st.markdown("### 📋 Recent Tasks")
    recent_tasks = tasks.sort_values('CreatedDate', ascending=False).head(10)
    display_cols = ['TaskID', 'Title', 'Department', 'AssignedTo', 'Status', 'Deadline']
    st.dataframe(recent_tasks[display_cols], use_container_width=True)

# ============= TAB 2: ALL TASKS =============
with tabs[1]:
    st.markdown("### 📝 All Tasks")
    
    col1, col2 = st.columns(2)
    with col1:
        status_filter = st.multiselect("Status", options=tasks['Status'].unique(), default=tasks['Status'].unique())
    with col2:
        dept_filter = st.multiselect("Department", options=tasks['Department'].unique(), default=tasks['Department'].unique())
    
    filtered_tasks = tasks[
        (tasks['Status'].isin(status_filter)) &
        (tasks['Department'].isin(dept_filter))
    ]
    
    # Display checkboxes for each task
    task_ids_to_delete = []
    for i, task in filtered_tasks.iterrows():
        # Use a fallback if TaskID is NaN or invalid
        task_id = task['TaskID'] if pd.notna(task['TaskID']) else f"Unknown_{i}"
    
        # Create a unique key for each checkbox using task_id and index
        checkbox = st.checkbox(f"Delete task {task['TaskID']} - {task['Title']}", key=f"{task_id}_{i}")
    
        if checkbox:
            task_ids_to_delete.append(task['TaskID'])

    # Display the filtered tasks in a table
    st.dataframe(filtered_tasks, use_container_width=True)

    # Add a button to delete selected tasks
    if task_ids_to_delete:
        if st.button("Delete selected tasks"):
            try:
                # Delete tasks from the DataFrame
                tasks_to_keep = tasks[~tasks['TaskID'].isin(task_ids_to_delete)]
                
                # Save the updated tasks back to Excel
                with pd.ExcelWriter(MOM_FILE, mode='a', if_sheet_exists='replace', engine='openpyxl') as writer:
                    tasks_to_keep.to_excel(writer, sheet_name='Tasks', index=False)
                
                st.success(f"✅ Successfully deleted {len(task_ids_to_delete)} task(s)!")
                st.cache_data.clear()
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error deleting tasks: {e}")
    else:
        st.write("No tasks selected for deletion.")

# ============= TAB 3: BOSS-MOM =============
with tabs[2]:
    st.markdown("### 👔 Boss-MoM Tasks")
    
    # FIX: Handle missing Category column gracefully
    if 'Category' in tasks.columns:
        boss_tasks = tasks[tasks['Category'] == 'Boss-MoM']
    else:
        boss_tasks = tasks[tasks['Title'].astype(str).str.contains('Boss', case=False, na=False)]
    
    if len(boss_tasks) > 0:
        st.dataframe(boss_tasks, use_container_width=True)
    else:
        st.info("ℹ️ No Boss-MoM tasks found")

# ============= TAB 4: DEPARTMENTS =============
with tabs[3]:
    st.markdown("### 🏢 Department Dashboard")
    
    # Step 1: Ensure 'tasks' DataFrame is loaded correctly (as you already did above)
    tasks = pd.read_excel(MOM_FILE, sheet_name='Tasks')

    # Step 2: Group tasks by 'Department' and calculate 'Total' and 'Completed' counts
    dept_perf = tasks.groupby('Department').agg({
        'TaskID': 'count',  # Count total tasks
        'Status': lambda x: (x == 'completed').sum()  # Count completed tasks
    }).rename(columns={'TaskID': 'Total', 'Status': 'Completed'})

    # Ensure 'Completed' and 'Total' columns are numeric
    dept_perf['Completed'] = pd.to_numeric(dept_perf['Completed'], errors='coerce')
    dept_perf['Total'] = pd.to_numeric(dept_perf['Total'], errors='coerce')

    # Replace NaN values with 0 for 'Completed' and 1 for 'Total' (to avoid division by zero)
    dept_perf['Completed'] = dept_perf['Completed'].fillna(0)
    dept_perf['Total'] = dept_perf['Total'].fillna(1)  # Avoid division by zero

    # Calculate Completion % and round to 1 decimal place
    dept_perf['Completion %'] = (dept_perf['Completed'] / dept_perf['Total'] * 100).round(1)

    # Display the department performance stats
    st.dataframe(dept_perf, use_container_width=True)

# ============= TAB 5: ADD TASK =============
with tabs[4]:
    st.markdown("### ➕ Add New MoM Task")
    
    with st.form("add_task_form"):
        meeting_id = st.text_input("Meeting ID")
        title = st.text_input("Task Title *")
        details = st.text_area("Task Details")
        department = st.selectbox("Department", options=['Finance', 'Accounts Payable', 'HR', 'IT', 'Operations', 'General'])
        assigned_to = st.text_input("Assigned To *")
        deadline = st.date_input("Deadline")
        category = st.selectbox("Category", options=['Regular', 'Boss-MoM', 'Urgent'])
        
        submitted = st.form_submit_button("➕ Add Task")
        
        if submitted:
            if title and assigned_to:
                try:
                    add_task(
                        meeting_id=meeting_id,
                        title=title,
                        details=details,
                        department=department,
                        assigned_to=assigned_to,
                        created_by=os.getenv('OWNER_EMAIL', 'System'),
                        deadline=deadline,
                        category=category
                    )
                    st.success("✅ Task added successfully!")
                    st.cache_data.clear()
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {e}")
            else:
                st.warning("⚠️ Please fill required fields")

# ============= TAB 6: ESCALATIONS =============
with tabs[5]:
    st.markdown("### ⚠️ Escalation Log")
    st.dataframe(escalations, use_container_width=True)

# ============= TAB 7: AI MOM EXTRACTOR =============
with tabs[6]:
    st.markdown("### 🤖 AI MoM Extractor")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        st.error("❌ OPENAI_API_KEY not found")
        st.info("💡 Set OPENAI_API_KEY in .env file")
        st.stop()

    meeting_notes = st.text_area(
        "Meeting Notes",
        height=300,
        placeholder="Paste meeting minutes..."
    )

    if st.button("🔍 Extract Tasks with AI"):
        if meeting_notes.strip():
            with st.spinner("🤖 AI is extracting tasks..."):
                try:
                    client = OpenAI(api_key=api_key)

                    prompt = f"""
Extract actionable tasks.
Return ONLY valid JSON array like this:

[
  {{
    "title": "...",
    "details": "...",
    "assigned_to": "...",
    "department": "...",
    "deadline": "YYYY-MM-DD or TBD"
  }}
]

NOTES:
{meeting_notes}
"""

                    resp = client.chat.completions.create(
                        model=config["ai"]["model"],
                        messages=[
                            {"role": "system", "content": "You extract MoM tasks as structured JSON only."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.0
                    )

                    extracted = resp.choices[0].message.content.strip()
                    st.code(extracted, language="json")

                    # ✅ Remove markdown fences if present
                    if extracted.startswith("```"):
                        extracted = extracted.split("```")[1].strip()

                    tasks_list = json.loads(extracted)

                    st.dataframe(pd.DataFrame(tasks_list), use_container_width=True)

                    # ✅ STORE FOR SAVE BUTTON
                    st.session_state["ai_tasks"] = tasks_list

                except Exception as e:
                    st.error(f"❌ AI Error: {e}")

    # ✅ SAFE SAVE BUTTON (NO NAMEERROR NOW)
    if "ai_tasks" in st.session_state:
        if st.button("💾 Save All Extracted Tasks"):
            saved = 0

            for task in st.session_state["ai_tasks"]:
                deadline_str = str(task.get("deadline", "")).strip()

                if deadline_str.upper() in ["TBD", "", "NONE", "MONTHLY"]:
                    deadline_obj = datetime.today() + timedelta(days=7)
                else:
                    try:
                        deadline_obj = datetime.strptime(deadline_str, "%Y-%m-%d")
                    except:
                        deadline_obj = datetime.today() + timedelta(days=7)

                add_task(
                    meeting_id="AI-Extract",
                    title=task.get("title", "Untitled"),
                    details=task.get("details", ""),
                    department=task.get("department", "General"),
                    assigned_to=task.get("assigned_to", "Unassigned"),
                    created_by="AI-Agent",
                    deadline=deadline_obj,
                    category="Regular"
                )

                saved += 1

            st.success(f"✅ Successfully saved {saved} AI tasks!")
            del st.session_state["ai_tasks"]
            st.cache_data.clear()
            st.rerun()

# ============= TAB 8: EXECUTIVE =============
with tabs[7]:
    st.markdown("### 👤 Executive Dashboard")
    exec_tasks = tasks[tasks['AssignedTo'].astype(str).str.contains('Executive', case=False, na=False)]
    
    if len(exec_tasks) > 0:
        st.dataframe(exec_tasks, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", len(exec_tasks))
        with col2:
            st.metric("Pending", len(exec_tasks[exec_tasks['Status'] == 'pending']))
        with col3:
            st.metric("Completed", len(exec_tasks[exec_tasks['Status'] == 'completed']))
    else:
        st.info("ℹ️ No executive tasks")

# ============= TAB 9: MANAGER =============
with tabs[8]:
    st.markdown("### 👨‍💼 Manager Dashboard")
    mgr_tasks = tasks[tasks['AssignedTo'].astype(str).str.contains('Manager', case=False, na=False)]
    
    if len(mgr_tasks) > 0:
        st.dataframe(mgr_tasks, use_container_width=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total", len(mgr_tasks))
        with col2:
            st.metric("Pending", len(mgr_tasks[mgr_tasks['Status'] == 'pending']))
        with col3:
            st.metric("Completed", len(mgr_tasks[mgr_tasks['Status'] == 'completed']))
    else:
        st.info("ℹ️ No manager tasks")

# ============= TAB 10: PERFORMANCE =============
with tabs[9]:
    st.markdown("### 📈 Performance Scorecard")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        completion_rate = (len(tasks[tasks['Status'] == 'completed']) / len(tasks) * 100) if len(tasks) > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    with col2:
        today = pd.Timestamp.now().normalize()
        overdue_count = len(tasks[(tasks['Status'] == 'pending') & (tasks['Deadline'] < today)])
        st.metric("Overdue", overdue_count)
    
    with col3:
        st.metric("Avg Time", "N/A")
    
    with col4:
        st.metric("Active Users", tasks['AssignedTo'].nunique())
    
    st.markdown("---")
    st.markdown("#### 🏢 Department Performance")
    
    dept_perf = tasks.groupby('Department').agg({
        'TaskID': 'count',
        'Status': lambda x: (x == 'completed').sum()
    }).rename(columns={'TaskID': 'Total', 'Status': 'Completed'})
    
    dept_perf['Pending'] = dept_perf['Total'] - dept_perf['Completed']
    dept_perf['Completion %'] = (dept_perf['Completed'] / dept_perf['Total'] * 100).round(1)
    
    st.dataframe(dept_perf, use_container_width=True)
