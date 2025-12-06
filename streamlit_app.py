import streamlit as st
import pandas as pd
from datetime import date
import yaml
from pdf_user_score import generate_user_score_pdf
from pdf_department_summary import generate_department_summary

st.markdown("""
<style>
/* Global background */
body {
    background-color: #111 !important;
    color: white !important;
}

/* Title color */
h2, h3, h4 {
    color: #e34234 !important;  /* Koenig Red */
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #202020 !important;
    color: white !important;
}

/* DataFrame style */
[data-testid="stDataFrame"] table {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

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
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1">
""", unsafe_allow_html=True)

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
# LOAD EXCEL sheets (with auto-clean + auto-create + sample data)
# ============================================================

import os

def ensure_excel_exists():
    """Auto-create Excel with correct structure + sample data."""
    if not os.path.exists(MOM_FILE):
        st.warning("MoM_Master.xlsx not found — creating a new one with sample data...")

        sample_users = pd.DataFrame([
            {"UserID": 1, "Name": "Praveen Chaudhary", "Email": "praveen.chaudhary@koenig-solutions.com",
             "Department": "EA-Director’s Office", "Role": "Manager"},
            {"UserID": 2, "Name": "Test Executive", "Email": "praveen.chaudhary@koenig-solutions.com",
             "Department": "Accounts/Finance", "Role": "Executive"},
        ])

        sample_tasks = pd.DataFrame([
            {
                "TaskID": 1, "MeetingID": 1, "Title": "Sample Task 1", "Details": "Setup MoM Testing",
                "Department": "EA-Director’s Office", "AssignedTo": 1,
                "CreatedBy": 1, "CreatedDate": date.today(),
                "Deadline": date.today(), "Status": "pending",
                "LastUpdateDate": "", "LastUpdateBy": ""
            },
            {
                "TaskID": 2, "MeetingID": 1, "Title": "Sample Pending Task",
                "Details": "This is a demo", "Department": "Accounts/Finance",
                "AssignedTo": 2, "CreatedBy": 1, "CreatedDate": date.today(),
                "Deadline": date.today(), "Status": "completed",
                "LastUpdateDate": "", "LastUpdateBy": ""
            }
        ])

        sample_meetings = pd.DataFrame([{"MeetingID": 1, "Title": "Boss Review Meeting"}])
        sample_logs = pd.DataFrame([{"LogID": 1, "TaskID": 1, "Action": "created", "Timestamp": date.today(), "Actor": "System"}])
        sample_esc = pd.DataFrame([{"EscID": 1, "TaskID": 1, "Level": 1, "Date": date.today()}])

        with pd.ExcelWriter(MOM_FILE, engine="openpyxl") as writer:
            sample_users.to_excel(writer, index=False, sheet_name="Users")
            sample_tasks.to_excel(writer, index=False, sheet_name="Tasks")
            sample_meetings.to_excel(writer, index=False, sheet_name="Meetings")
            sample_logs.to_excel(writer, index=False, sheet_name="Logs")
            sample_esc.to_excel(writer, index=False, sheet_name="Escalations")

def load_sheets():
    ensure_excel_exists()  # Auto-create + sample data

    users = pd.read_excel(MOM_FILE, sheet_name="Users")
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    meetings = pd.read_excel(MOM_FILE, sheet_name="Meetings")
    logs = pd.read_excel(MOM_FILE, sheet_name="Logs")
    esc = pd.read_excel(MOM_FILE, sheet_name="Escalations")

    # Auto strip spaces
    for df in [users, tasks, meetings, logs, esc]:
        df.columns = df.columns.str.strip()

    return users, tasks, meetings, logs, esc


# Load into memory
try:
    users, tasks, meetings, logs, esc = load_sheets()

    # CLEAN COLUMN SPACES
    tasks.columns = tasks.columns.str.strip()
    users.columns = users.columns.str.strip()
    meetings.columns = meetings.columns.str.strip()
    logs.columns = logs.columns.str.strip()
    esc.columns = esc.columns.str.strip()

    # FIX: Convert Deadline to date
    tasks["Deadline"] = pd.to_datetime(tasks["Deadline"], errors="coerce").dt.date

except Exception as e:
    st.error(f"❌ Failed to load Excel data: {e}")
    st.stop()

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

tab8 = st.tabs(["👤 Executive Dashboard"])[0]

with tab8:
    st.header("👤 Executive Dashboard")

    executive_name = st.selectbox("Select Executive", users["Name"])

    user_id = int(users[users["Name"] == executive_name]["UserID"].iloc[0])

    my_tasks = tasks[tasks["AssignedTo"] == user_id]

    col1, col2, col3 = st.columns(3)
    col1.metric("Assigned Tasks", len(my_tasks))
    col2.metric("Completed", len(my_tasks[my_tasks["Status"] == "completed"]))
    col3.metric("Overdue", len(my_tasks[(my_tasks["Deadline"] < date.today()) & (my_tasks["Status"] == "pending")]))

    st.subheader("My Pending Tasks")
    st.dataframe(my_tasks[my_tasks["Status"] == "pending"])

tab9 = st.tabs(["🧑‍💼 Manager Dashboard"])[0]

with tab9:
    st.header("🧑‍💼 Manager Dashboard")

    manager_name = st.selectbox("Select Manager", users[users["Role"] == "Manager"]["Name"])

    manager_id = int(users[users["Name"] == manager_name]["UserID"].iloc[0])
    manager_dept = users[users["UserID"] == manager_id]["Department"].iloc[0]

    dept_users = users[users["Department"] == manager_dept]
    dept_user_ids = dept_users["UserID"].tolist()

    dept_tasks = tasks[tasks["AssignedTo"].isin(dept_user_ids)]

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Team Size", len(dept_users))
    col2.metric("Team Tasks", len(dept_tasks))
    col3.metric("Completed", len(dept_tasks[dept_tasks["Status"] == "completed"]))
    col4.metric("Overdue", len(dept_tasks[(dept_tasks["Deadline"] < date.today()) & (dept_tasks["Status"] == "pending")]))

    st.subheader("Department Task Table")
    st.dataframe(dept_tasks)

tab10 = st.tabs(["📈 Performance Scorecard"])[0]

with tab10:
    st.header("📈 Executive MoM Scorecard")

    scores = []

    for _, user in users.iterrows():
        uid = user["UserID"]
        name = user["Name"]

        user_tasks = tasks[tasks["AssignedTo"] == uid]

        if len(user_tasks) == 0:
            continue

        completion_rate = len(user_tasks[user_tasks["Status"] == "completed"]) / len(user_tasks) * 100
        overdue = len(user_tasks[(user_tasks["Deadline"] < date.today()) & (user_tasks["Status"] == "pending")])
        score = max(0, 100 - overdue * 5) * (completion_rate / 100)

        scores.append({
            "Name": name,
            "Department": user["Department"],
            "Score": round(score, 2),
            "Tasks": len(user_tasks),
            "Overdue": overdue
        })

    st.dataframe(pd.DataFrame(scores))

st.subheader("📄 Download User Performance Score PDF")

user_name = st.selectbox("Select Executive", users["Name"])

if st.button("Generate User Score PDF"):
    pdf_path = generate_user_score_pdf(user_name)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download PDF",
            data=f,
            mime="application/pdf",
            file_name="UserScore.pdf"
        )

st.subheader("📄 Download Department Summary PDF")

dept_name = st.selectbox("Select Department", users["Department"].unique())

if st.button("Generate Department PDF"):
    pdf_path = generate_department_summary(dept_name)
    with open(pdf_path, "rb") as f:
        st.download_button(
            label="📥 Download PDF",
            data=f,
            mime="application/pdf",
            file_name="DepartmentSummary.pdf"
        )




