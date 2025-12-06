import streamlit as st
import pandas as pd
from datetime import date
import yaml

# ============================================================
# LOAD CONFIGURATION
# ============================================================

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
dashboard_title = config["branding"]["dashboard_title"]

MOM_FILE = config["paths"]["mom_file"]

# ============================================================
# PAGE SETUP
# ============================================================

st.set_page_config(
    page_title=dashboard_title,
    page_icon=logo_url,
    layout="wide"
)

# CENTERED LOGO HEADER
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.image(logo_url, width=160)
    st.markdown(
        f"<h2 style='text-align:center; margin-top:10px;'>{dashboard_title}</h2>",
        unsafe_allow_html=True,
    )

# SIDEBAR BRANDING
st.sidebar.image(logo_url, width=140)
st.sidebar.markdown("### Koenig Solutions – MoM Follow-Up System")

# ============================================================
# LOAD EXCEL sheets
# ============================================================

@st.cache_data
def load_sheets():
    users = pd.read_excel(MOM_FILE, sheet_name="Users")
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    meetings = pd.read_excel(MOM_FILE, sheet_name="Meetings")
    logs = pd.read_excel(MOM_FILE, sheet_name="Logs")
    esc = pd.read_excel(MOM_FILE, sheet_name="Escalations")
    return users, tasks, meetings, logs, esc

users, tasks, meetings, logs, esc = load_sheets()

# ============================================================
# TABS LAYOUT
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Dashboard",
    "📄 Tasks",
    "⭐ Boss-MoM",
    "🏢 Departments",
    "➕ Add Task",
    "🚨 Escalations",
    "🤖 AI MoM Extractor"
])

# ============================================================
# TAB 1 — DASHBOARD SUMMARY
# ============================================================

with tab1:
    st.header("📊 Overview Summary")

    total = len(tasks)
    pending = len(tasks[tasks["Status"] == "pending"])
    completed = len(tasks[tasks["Status"] == "completed"])
    overdue = len(tasks[(tasks["Deadline"] < date.today()) & (tasks["Status"] == "pending")])

    colA, colB, colC, colD = st.columns(4)
    colA.metric("Total Tasks", total)
    colB.metric("Pending", pending)
    colC.metric("Completed", completed)
    colD.metric("Overdue", overdue)

    st.subheader("Today's Pending Tasks")
    st.dataframe(tasks[tasks["Status"] == "pending"])

# ============================================================
# TAB 2 — ALL TASKS VIEW
# ============================================================

with tab2:
    st.header("📄 All Tasks")

    dept_filter = st.selectbox("Filter by Department", ["All"] + list(users["Department"].unique()))

    df = tasks.copy()
    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]

    st.dataframe(df, use_container_width=True)

# ============================================================
# TAB 3 — BOSS-MOM TASKS
# ============================================================

with tab3:
    st.header("⭐ Boss-MoM Tasks")

    boss_id = config["meetings"]["boss_meeting_id"]
    boss_tasks = tasks[tasks["MeetingID"] == boss_id]

    st.subheader("All Boss-MoM Tasks")
    st.dataframe(boss_tasks, use_container_width=True)

    overdue_boss = boss_tasks[
        (boss_tasks["Deadline"] < date.today()) & (boss_tasks["Status"] != "completed")
    ]

    st.subheader("🔥 Overdue Boss Tasks")
    st.dataframe(overdue_boss, use_container_width=True)

# ============================================================
# TAB 4 — DEPARTMENT-WISE VIEW
# ============================================================

with tab4:
    st.header("🏢 Department Dashboard")

    dept = st.selectbox("Select Department", users["Department"].unique())

    dept_users = users[users["Department"] == dept]
    st.subheader(f"Team Members – {dept}")
    st.dataframe(dept_users, use_container_width=True)

    dept_tasks = tasks[tasks["Department"] == dept]
    st.subheader(f"Tasks – {dept}")
    st.dataframe(dept_tasks, use_container_width=True)

# ============================================================
# TAB 5 — ADD TASK
# ============================================================

from mom_agent import add_task

with tab5:
    st.header("➕ Add New MoM Task")

    title = st.text_input("Task Title")
    details = st.text_area("Task Details")
    meeting_id = st.number_input("Meeting ID", min_value=1)
    department = st.selectbox("Assign to Department", users["Department"].unique())
    assigned_name = st.selectbox("Assign To (Executive/Manager)", users["Name"])
    deadline = st.date_input("Deadline")

    created_by = 999  # Admin user ID

    if st.button("Create Task"):
        assigned_id = int(users[users["Name"] == assigned_name]["UserID"].iloc[0])

        add_task(
            meeting_id=meeting_id,
            title=title,
            details=details,
            department=department,
            assigned_to=assigned_id,
            created_by=created_by,
            deadline=deadline
        )

        st.success("Task added successfully!")

# ============================================================
# TAB 6 — ESCALATION LOG
# ============================================================

with tab6:
    st.header("🚨 Escalation Log")
    st.dataframe(esc, use_container_width=True)

# ============================================================
# TAB 7 — AI MOM EXTRACTOR
# ============================================================

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

with tab7:
    st.header("🤖 AI MoM Extractor")
    st.write("Paste meeting notes below:")

    raw_notes = st.text_area("Meeting Notes", height=250)

    if st.button("Extract Tasks with AI"):
        prompt = f"""
        Extract actionable MoM tasks from the following text.

        Output JSON with fields:
        - title
        - details
        - department
        - assigned_to
        - deadline (YYYY-MM-DD or blank)

        Meeting Notes:
        {raw_notes}
        """

        response = openai.ChatCompletion.create(
            model=config["ai"]["model"],
            messages=[{"role": "user", "content": prompt}]
        )

        extracted = response["choices"][0]["message"]["content"]

        st.subheader("Extracted Tasks")
        st.json(extracted)

        st.session_state["ai_tasks"] = extracted

    if "ai_tasks" in st.session_state:
        if st.button("Save Extracted Tasks"):
            tasks_json = eval(st.session_state["ai_tasks"])

            for t in tasks_json:
                assigned_id = int(users[users["Name"] == t["assigned_to"]]["UserID"].iloc[0])

                add_task(
                    meeting_id=999,
                    title=t["title"],
                    details=t["details"],
                    department=t["department"],
                    assigned_to=assigned_id,
                    created_by=999,
                    deadline=t["deadline"] or date.today()
                )

            st.success("Extracted tasks saved successfully!")

