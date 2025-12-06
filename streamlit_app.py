import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
import yaml
from pdf_user_score import generate_user_score_pdf
from pdf_department_summary import generate_department_summary
from monthly_summary_pdf import generate_monthly_pdf

# -------------------------------
# DARK THEME CSS
# -------------------------------
st.markdown("""
<style>
body { background-color: #111 !important; color: white !important; }
h2, h3, h4 { color: #e34234 !important; }
[data-testid="stSidebar"] { background-color: #202020 !important; }
[data-testid="stDataFrame"] table { color: white !important; }
</style>
""", unsafe_allow_html=True)

# -------------------------------
# LOAD CONFIG
# -------------------------------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
dashboard_title = config["branding"]["dashboard_title"]
MOM_FILE = config["paths"]["mom_file"]

# -------------------------------
# AUTO-CREATE EXCEL IF NOT EXISTS
# -------------------------------
def create_empty_excel():
    # Create folder if missing
    os.makedirs(os.path.dirname(MOM_FILE), exist_ok=True)

    df_users = pd.DataFrame({
        "UserID": [1],
        "Name": ["Praveen Chaudhary"],
        "Email": ["praveen.chaudhary@koenig-solutions.com"],
        "Role": ["Manager"],
        "Department": ["Management"]
    })

    df_tasks = pd.DataFrame({
        "TaskID": [1],
        "MeetingID": [1],
        "Title": ["Sample Task"],
        "Details": ["This is a demo task."],
        "Department": ["Management"],
        "AssignedTo": [1],
        "CreatedBy": [1],
        "CreatedDate": [date.today()],
        "Deadline": [date.today()],
        "Status": ["pending"],
        "LastUpdateDate": [""],
        "LastUpdateBy": [""]
    })

    df_meetings = pd.DataFrame({"MeetingID": [1], "Description": ["Sample Meeting"]})
    df_logs = pd.DataFrame({"LogID": [], "TaskID": [], "Action": [], "Timestamp": [], "Actor": []})
    df_esc = pd.DataFrame({"EscID": [], "TaskID": [], "Level": [], "Timestamp": [], "Actor": []})

    with pd.ExcelWriter(MOM_FILE) as writer:
        df_users.to_excel(writer, index=False, sheet_name="Users")
        df_tasks.to_excel(writer, index=False, sheet_name="Tasks")
        df_meetings.to_excel(writer, index=False, sheet_name="Meetings")
        df_logs.to_excel(writer, index=False, sheet_name="Logs")
        df_esc.to_excel(writer, index=False, sheet_name="Escalations")


if not os.path.exists(MOM_FILE):
    create_empty_excel()

# -------------------------------
# LOAD SHEETS SAFELY
# -------------------------------
def load_sheets():
    try:
        users = pd.read_excel(MOM_FILE, sheet_name="Users")
        tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
        meetings = pd.read_excel(MOM_FILE, sheet_name="Meetings")
        logs = pd.read_excel(MOM_FILE, sheet_name="Logs")
        esc = pd.read_excel(MOM_FILE, sheet_name="Escalations")

        # Clean column names
        users.columns = users.columns.str.strip()
        tasks.columns = tasks.columns.str.strip()
        meetings.columns = meetings.columns.str.strip()
        logs.columns = logs.columns.str.strip()
        esc.columns = esc.columns.str.strip()

        # DATE FIX
        if "Deadline" in tasks.columns:
            tasks["Deadline"] = pd.to_datetime(tasks["Deadline"]).dt.date

        if "CreatedDate" in tasks.columns:
            tasks["CreatedDate"] = pd.to_datetime(tasks["CreatedDate"]).dt.date

        return users, tasks, meetings, logs, esc
    except Exception as e:
        st.error(f"Error loading Excel: {e}")
        st.stop()

users, tasks, meetings, logs, esc = load_sheets()

# -------------------------------
# PAGE HEADER
# -------------------------------
st.set_page_config(page_title=dashboard_title, layout="wide")
st.image(logo_url, width=160)
st.markdown(f"<h2 style='text-align:center;'>{dashboard_title}</h2>", unsafe_allow_html=True)

# -------------------------------
# TABS
# -------------------------------
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Dashboard",
    "📄 Tasks",
    "⭐ Boss-MoM",
    "🏢 Departments",
    "📈 Performance",
    "📄 PDF Reports"
])

# -------------------------------
# TAB 1 — DASHBOARD
# -------------------------------
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
    st.dataframe(tasks[tasks["Status"] == "pending"], use_container_width=True)

# -------------------------------
# TAB 2 — ALL TASKS
# -------------------------------
with tab2:
    st.header("📄 All Tasks")
    dept_filter = st.selectbox("Filter by Department", ["All"] + list(users["Department"].unique()), key="dept_tasks")
    df = tasks.copy()
    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]
    st.dataframe(df, use_container_width=True)

# -------------------------------
# TAB 3 — BOSS MOM
# -------------------------------
with tab3:
    boss_id = config["meetings"]["boss_meeting_id"]
    st.header("⭐ Boss-MoM Tasks")
    boss_tasks = tasks[tasks["MeetingID"] == boss_id]
    st.dataframe(boss_tasks, use_container_width=True)

# -------------------------------
# TAB 4 — DEPARTMENTS
# -------------------------------
with tab4:
    st.header("🏢 Department Dashboard")
    dept = st.selectbox("Select Department", users["Department"].unique(), key="dept_dashboard")
    dept_users = users[users["Department"] == dept]
    dept_tasks = tasks[tasks["Department"] == dept]

    st.subheader("Team Members")
    st.dataframe(dept_users)
    st.subheader("Tasks")
    st.dataframe(dept_tasks)

# -------------------------------
# TAB 5 — PERFORMANCE
# -------------------------------
with tab5:
    st.header("📈 Performance Scorecard")

    scores = []
    for _, user in users.iterrows():
        uid = user["UserID"]
        name = user["Name"]

        user_tasks = tasks[tasks["AssignedTo"] == uid]
        if len(user_tasks) == 0:
            continue

        completion = len(user_tasks[user_tasks["Status"] == "completed"])
        overdue = len(user_tasks[(user_tasks["Deadline"] < date.today()) & (user_tasks["Status"] == "pending")])
        completion_rate = completion / len(user_tasks) * 100
        score = max(0, 100 - overdue * 5) * (completion_rate / 100)

        scores.append({
            "Name": name,
            "Score": round(score, 2),
            "Tasks": len(user_tasks),
            "Overdue": overdue
        })

    st.dataframe(pd.DataFrame(scores))

# -------------------------------
# TAB 6 — PDF REPORTS
# -------------------------------
with tab6:
    st.header("📄 PDF Reports")

    st.subheader("User Performance PDF")
    user_name = st.selectbox("Select Executive", users["Name"], key="user_pdf")
    if st.button("Generate User PDF"):
        pdf_path = generate_user_score_pdf(user_name)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name="UserScore.pdf")

    st.subheader("Department Summary PDF")
    dept_name = st.selectbox("Select Department", users["Department"].unique(), key="dept_pdf")
    if st.button("Generate Dept PDF"):
        pdf_path = generate_department_summary(dept_name)
        with open(pdf_path, "rb") as f:
            st.download_button("📥 Download PDF", f, file_name="DeptSummary.pdf")

st.subheader("📅 Download Monthly MoM Summary PDF")

if st.button("Generate Monthly PDF"):
    pdf = generate_monthly_pdf()
    with open(pdf, "rb") as f:
        st.download_button(
            label="📥 Download Monthly PDF",
            data=f,
            file_name="Monthly_MoM_Summary.pdf",
            mime="application/pdf"
        )

