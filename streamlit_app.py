import streamlit as st
import pandas as pd
from datetime import date, datetime
import os

MOM_FILE = "/Users/praveenchaudhary/Library/CloudStorage/OneDrive-KoenigSolutionsLtd/MoM/MoM_Master.xlsx"

# ---------------------------------------------------------
# Load Sheets
# ---------------------------------------------------------

def load_data():
    users = pd.read_excel(MOM_FILE, sheet_name="Users")
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    meetings = pd.read_excel(MOM_FILE, sheet_name="Meetings")
    logs = pd.read_excel(MOM_FILE, sheet_name="Logs")
    esc = pd.read_excel(MOM_FILE, sheet_name="Escalations")
    return users, tasks, meetings, logs, esc

# ---------------------------------------------------------
# Streamlit UI Layout
# ---------------------------------------------------------

st.set_page_config(page_title="Koenig MoM Dashboard", layout="wide")
st.title("📘 Koenig MoM Dashboard")
st.caption("Meeting Minutes Tracker – Automated Follow-Up System")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Dashboard",
    "Tasks",
    "Boss MoM",
    "Departments",
    "Add Task",
    "Escalations"
])

users, tasks, meetings, logs, esc = load_data()

with tab1:
    st.header("📊 Overview")

    total_tasks = len(tasks)
    pending = len(tasks[tasks["Status"] == "pending"])
    completed = len(tasks[tasks["Status"] == "completed"])
    overdue = len(tasks[(tasks["Deadline"] < date.today()) & (tasks["Status"] == "pending")])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks", total_tasks)
    col2.metric("Pending", pending)
    col3.metric("Completed", completed)
    col4.metric("Overdue", overdue)

    st.write("### Today's Pending Tasks")
    st.dataframe(tasks[tasks["Status"] == "pending"])

with tab2:
    st.header("📄 All Tasks")
    dept_filter = st.selectbox("Filter by Department", ["All"] + list(users["Department"].unique()))

    df = tasks.copy()
    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]

    st.dataframe(df)

with tab3:
    st.header("⭐ Boss MoM Tasks")
    boss_tasks = tasks[tasks["MeetingID"] == 1]
    st.dataframe(boss_tasks)

    overdue_boss = boss_tasks[(boss_tasks["Deadline"] < date.today()) & (boss_tasks["Status"] != "completed")]
    st.write("### 🔥 Overdue Boss Tasks")
    st.dataframe(overdue_boss)

with tab4:
    st.header("🏢 Department View")

    dept = st.selectbox("Select Department", users["Department"].unique())
    dept_users = users[users["Department"] == dept]

    st.subheader(f"Team Members – {dept}")
    st.dataframe(dept_users)

    dept_tasks = tasks[tasks["Department"] == dept]
    st.subheader(f"Tasks – {dept}")
    st.dataframe(dept_tasks)

with tab5:
    st.header("➕ Add New Task")

    title = st.text_input("Task Title")
    details = st.text_area("Task Details")
    meeting_id = st.number_input("Meeting ID", min_value=1)
    department = st.selectbox("Assign Department", users["Department"].unique())
    assigned_user = st.selectbox("Assign To Executive/Manager", users["Name"])
    deadline = st.date_input("Deadline")

    created_by = 999  # Your user ID (Admin)

    if st.button("Add Task"):
        user_id = int(users[users["Name"] == assigned_user]["UserID"])
        from mom_agent import add_task   # Import from automation engine
        
        add_task(
            meeting_id=meeting_id,
            title=title,
            details=details,
            department=department,
            assigned_to=user_id,
            created_by=created_by,
            deadline=deadline
        )
        st.success("Task added successfully!")

with tab6:
    st.header("🚨 Escalation Log")
    st.dataframe(esc)

tab7 = st.tabs(["AI MoM Extractor"])[0]

with tab7:
    st.header("🤖 AI MoM Extractor")

    raw_notes = st.text_area("Paste your meeting notes here:", height=300)

    if st.button("Extract Tasks"):
        import openai

        openai.api_key = os.getenv("OPENAI_API_KEY")

        prompt = f"""
        You are an MoM Extraction Assistant.

        Extract tasks in JSON from these meeting notes:

        {raw_notes}
        """

        response = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}]
        )

        result_text = response["choices"][0]["message"]["content"]

        st.subheader("Extracted Tasks (Review before saving)")
        st.json(result_text)

        st.session_state["extracted_tasks"] = result_text

if "extracted_tasks" in st.session_state:
    if st.button("Save Tasks to MoM System"):
        tasks_json = eval(st.session_state["extracted_tasks"])

        from mom_agent import add_task
        
        for t in tasks_json:
            assigned_name = t["assigned_to"]
            dept = t["department"]
            deadline = t["deadline"]

            assigned_id = int(users[users["Name"] == assigned_name]["UserID"].iloc[0])

            add_task(
                meeting_id=999,  # Auto-meeting ID for extracted notes
                title=t["title"],
                details=t["details"],
                department=dept,
                assigned_to=assigned_id,
                created_by=999,  # Admin user
                deadline=deadline if deadline else date.today()
            )

        st.success("All extracted tasks saved successfully!")
