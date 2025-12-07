import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
import yaml
from pdf_user_score import generate_user_score_pdf
from pdf_department_summary import generate_department_summary
from monthly_summary_pdf import generate_monthly_pdf
from PIL import Image

# ============================================================
# ✅ PAGE CONFIG — MUST BE FIRST STREAMLIT COMMAND
# ============================================================

st.set_page_config(
    page_title="Koenig MoM Automation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ✅ LOAD CONFIG AFTER PAGE CONFIG
# ============================================================

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
dashboard_title = config["branding"]["dashboard_title"]
MOM_FILE = config["paths"]["mom_file"]

# ============================================================
# ✅ CUSTOM DARK THEME + FIXED SIDEBAR VISIBILITY
# ============================================================

st.markdown("""
<style>
body {
    background-color: #111 !important;
    color: white !important;
}
h1, h2, h3, h4 {
    color: #e34234 !important;
}

/* Sidebar - lighter for better visibility */
[data-testid="stSidebar"] {
    background-color: #2b2b2b !important;
    color: white !important;
}

/* Sidebar text fix */
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Dataframe text */
[data-testid="stDataFrame"] table {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ✅ MAIN HEADER — LOGO ABOVE, TITLE BELOW (PERFECTLY CENTERED)
# ============================================================

st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center;">
    <img src="{logo_url}" width="160">
    <h2 style='margin-top:10px; color:#e34234;'>{dashboard_title}</h2>
</div>
<hr style='border:1px solid #e34234'>
""", unsafe_allow_html=True)

# ============================================================
# ✅ CLEAN PROFESSIONAL SIDEBAR (NO LOGO HERE)
# ============================================================

st.sidebar.markdown("## 🤖 Koenig MoM Agent")
st.sidebar.markdown("""
✅ Track all MoM actions  
✅ Monitor overdue tasks  
✅ Generate performance reports  
✅ Auto-email summaries  
✅ Maintain full accountability  

---
📌 **Status:** Live & Active  
📊 **Mode:** Automation  
🛡 **Owner:** Koenig Automation  
""")

# ============================================================
# ✅ LOAD EXCEL SAFELY
# ============================================================

def load_sheets():
    users = pd.read_excel(MOM_FILE, sheet_name="Users")
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    meetings = pd.read_excel(MOM_FILE, sheet_name="Meetings")
    logs = pd.read_excel(MOM_FILE, sheet_name="Logs")
    esc = pd.read_excel(MOM_FILE, sheet_name="Escalations")

    # ✅ CLEAN COLUMN NAMES
    for df in [users, tasks, meetings, logs, esc]:
        df.columns = df.columns.str.strip()

    # ✅ FIX DATE TYPES
    tasks["Deadline"] = pd.to_datetime(tasks["Deadline"], errors="coerce")

    return users, tasks, meetings, logs, esc

users, tasks, meetings, logs, esc = load_sheets()

# ============================================================
# ✅ CREATE ALL TABS (1–10)
# ============================================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9, tab10 = st.tabs([
    "📊 Dashboard",
    "📄 Tasks",
    "⭐ Boss-MoM",
    "🏢 Departments",
    "➕ Add Task",
    "🚨 Escalations",
    "🤖 AI MoM Extractor",
    "👤 Executive Dashboard",
    "🧑‍💼 Manager Dashboard",
    "📈 Performance Scorecard"
])

# ============================================================
# ✅ TAB 1 — DASHBOARD
# ============================================================

with tab1:
    st.header("📊 Overview Summary")

    total = len(tasks)
    pending = len(tasks[tasks["Status"] == "pending"])
    completed = len(tasks[tasks["Status"] == "completed"])
    overdue = len(tasks[(tasks["Deadline"] < pd.to_datetime(date.today())) & (tasks["Status"] == "pending")])

    colA, colB, colC, colD = st.columns(4)
    colA.metric("Total Tasks", total)
    colB.metric("Pending", pending)
    colC.metric("Completed", completed)
    colD.metric("Overdue", overdue)

    st.subheader("Today's Pending Tasks")
    st.dataframe(tasks[tasks["Status"] == "pending"])

# ============================================================
# ✅ TAB 2 — TASKS
# ============================================================

with tab2:
    st.header("📄 All Tasks")
    dept_filter = st.selectbox("Filter by Department", ["All"] + list(users["Department"].unique()), key="dept_filter")

    df = tasks.copy()
    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]

    st.dataframe(df)

# ============================================================
# ✅ TAB 3 — BOSS MOM
# ============================================================

with tab3:
    st.header("⭐ Boss-MoM Tasks")
    boss_id = config["meetings"]["boss_meeting_id"]

    boss_tasks = tasks[tasks["MeetingID"] == boss_id]
    st.dataframe(boss_tasks)

# ============================================================
# ✅ TAB 4 — DEPARTMENTS
# ============================================================

with tab4:
    dept = st.selectbox("Select Department", users["Department"].unique(), key="dept_sel")
    st.dataframe(tasks[tasks["Department"] == dept])

# ============================================================
# ✅ TAB 6 — ESCALATIONS
# ============================================================

with tab6:
    st.dataframe(esc)

# ============================================================
# ✅ TAB 8 — EXECUTIVE DASHBOARD
# ============================================================

with tab8:
    executive_name = st.selectbox("Select Executive", users["Name"], key="exec_sel")
    user_id = int(users[users["Name"] == executive_name]["UserID"].iloc[0])

    my_tasks = tasks[tasks["AssignedTo"] == user_id]
    st.dataframe(my_tasks)

# ============================================================
# ✅ TAB 9 — MANAGER DASHBOARD
# ============================================================

with tab9:
    manager_name = st.selectbox("Select Manager", users["Name"], key="mgr_sel")
    st.dataframe(tasks)

# ============================================================
# ✅ TAB 10 — PERFORMANCE SCORECARD
# ============================================================

with tab10:
    scores = []
    for _, user in users.iterrows():
        uid = user["UserID"]
        name = user["Name"]
        user_tasks = tasks[tasks["AssignedTo"] == uid]

        if len(user_tasks) == 0:
            continue

        completion_rate = len(user_tasks[user_tasks["Status"] == "completed"]) / len(user_tasks) * 100
        overdue = len(user_tasks[(user_tasks["Deadline"] < pd.to_datetime(date.today())) & (user_tasks["Status"] == "pending")])
        score = round(max(0, 100 - overdue * 5) * (completion_rate / 100), 2)

        scores.append({"Name": name, "Score": score})

    st.dataframe(pd.DataFrame(scores))

# ============================================================
# ✅ PDF DOWNLOADS WITH UNIQUE KEYS
# ============================================================

st.subheader("📄 Download User Performance Score PDF")
user_name = st.selectbox("Select Executive", users["Name"], key="pdf_exec")
if st.button("Generate User Score PDF", key="pdf_exec_btn"):
    pdf_path = generate_user_score_pdf(user_name)
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, file_name="UserScore.pdf", key="pdf_exec_dl")

st.subheader("📄 Download Department Summary PDF")
dept_name = st.selectbox("Select Department", users["Department"].unique(), key="pdf_dept")
if st.button("Generate Department PDF", key="pdf_dept_btn"):
    pdf_path = generate_department_summary(dept_name)
    with open(pdf_path, "rb") as f:
        st.download_button("Download PDF", f, file_name="DepartmentSummary.pdf", key="pdf_dept_dl")
