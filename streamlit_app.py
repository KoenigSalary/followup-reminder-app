import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
import yaml
from pdf_user_score import generate_user_score_pdf
from pdf_department_summary import generate_department_summary
from monthly_summary_pdf import generate_monthly_pdf

# ============================================================
# ✅ PAGE CONFIG — MUST BE FIRST STREAMLIT COMMAND
# ============================================================

st.set_page_config(
    page_title="Koenig MoM Automation Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# ✅ LOAD CONFIG
# ============================================================

with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
dashboard_title = config["branding"]["dashboard_title"]
MOM_FILE = config["paths"].get("mom_file", "data/MoM_Master.xlsx")

# ============================================================
# ✅ CUSTOM THEME (BLUE TITLE LIKE LOGO)
# ============================================================

st.markdown("""
<style>
body {
    background-color: #f8f8f8 !important;
}
h1, h2, h3, h4 {
    color: #005BAA !important;  /* Koenig blue-ish */
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #222 !important;
    color: white !important;
}
[data-testid="stSidebar"] * {
    color: white !important;
}

/* Dataframe text */
[data-testid="stDataFrame"] table {
    color: #111 !important;
}

/* Tabs underline color */
[data-baseweb="tab-list"] > div[aria-selected="true"] {
    border-bottom: 3px solid #e34234 !important;
}
</style>
""", unsafe_allow_html=True)

# ============================================================
# ✅ MAIN HEADER — CENTERED LOGO THEN TITLE
# ============================================================

st.markdown("<div style='height:15px'></div>", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    st.markdown(
        f"<div style='text-align:center;'><img src='{logo_url}' width='170'></div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h2 style='text-align:center; margin-top:10px;'>{dashboard_title}</h2>",
        unsafe_allow_html=True,
    )

st.markdown("<hr style='border:1px solid #e34234'>", unsafe_allow_html=True)

# ============================================================
# ✅ SIDEBAR
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
# ✅ LOAD EXCEL SHEETS
# ============================================================

@st.cache_data
def load_sheets(path: str):
    if not os.path.exists(path):
        return None, None, None, None, None

    xl_users = pd.read_excel(path, sheet_name="Users")
    xl_tasks = pd.read_excel(path, sheet_name="Tasks")
    xl_meetings = pd.read_excel(path, sheet_name="Meetings")
    xl_logs = pd.read_excel(path, sheet_name="Logs")
    xl_esc = pd.read_excel(path, sheet_name="Escalations")

    # Strip column spaces
    for df in [xl_users, xl_tasks, xl_meetings, xl_logs, xl_esc]:
        df.columns = df.columns.str.strip()

    # Convert date columns in Tasks
    if "Deadline" in xl_tasks.columns:
        xl_tasks["Deadline"] = pd.to_datetime(xl_tasks["Deadline"], errors="coerce")
    if "CreatedDate" in xl_tasks.columns:
        xl_tasks["CreatedDate"] = pd.to_datetime(xl_tasks["CreatedDate"], errors="coerce")
    if "LastUpdateDate" in xl_tasks.columns:
        xl_tasks["LastUpdateDate"] = pd.to_datetime(xl_tasks["LastUpdateDate"], errors="coerce")

    return xl_users, xl_tasks, xl_meetings, xl_logs, xl_esc


users, tasks, meetings, logs, esc = load_sheets(MOM_FILE)

if users is None:
    st.error(f"MoM file not found at: {MOM_FILE}. Please upload/commit the Excel and update config.yaml.")
    st.stop()

# ============================================================
# ✅ IMPORT MOM AGENT HELPERS
# ============================================================

from mom_agent import add_task  # uses same MOM_FILE internally

# ============================================================
# ✅ CREATE TABS (1–10)
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
# TAB 1 — DASHBOARD
# ============================================================

with tab1:
    st.header("📊 Overview Summary")

    today = pd.to_datetime(date.today())

    total = len(tasks)
    pending = len(tasks[tasks["Status"] == "pending"])
    completed = len(tasks[tasks["Status"] == "completed"])
    overdue = len(tasks[(tasks["Deadline"] < today) & (tasks["Status"] == "pending")])

    cA, cB, cC, cD = st.columns(4)
    cA.metric("Total Tasks", total)
    cB.metric("Pending", pending)
    cC.metric("Completed", completed)
    cD.metric("Overdue", overdue)

    st.subheader("Today's Pending Tasks")
    today_pending = tasks[
        (tasks["Status"] == "pending") &
        (tasks["Deadline"].dt.date == date.today())
    ]
    st.dataframe(today_pending if not today_pending.empty else tasks[tasks["Status"] == "pending"])

# ============================================================
# TAB 2 — ALL TASKS
# ============================================================

with tab2:
    st.header("📄 All Tasks")

    dept_filter = st.selectbox(
        "Filter by Department",
        ["All"] + sorted(users["Department"].unique().tolist()),
        key="dept_filter_all"
    )

    df = tasks.copy()
    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]

    st.dataframe(df, use_container_width=True)

# ============================================================
# TAB 3 — BOSS-MoM
# ============================================================

with tab3:
    st.header("⭐ Boss-MoM Tasks")

    boss_id = config["meetings"]["boss_meeting_id"]
    boss_tasks = tasks[tasks["MeetingID"] == boss_id]

    st.subheader("All Boss-MoM Tasks")
    st.dataframe(boss_tasks, use_container_width=True)

    today = pd.to_datetime(date.today())
    overdue_boss = boss_tasks[
        (boss_tasks["Deadline"] < today) &
        (boss_tasks["Status"] != "completed")
    ]

    st.subheader("🔥 Overdue Boss Tasks")
    st.dataframe(overdue_boss, use_container_width=True)

# ============================================================
# TAB 4 — DEPARTMENTS
# ============================================================

with tab4:
    st.header("🏢 Department Dashboard")

    dept = st.selectbox(
        "Select Department",
        sorted(users["Department"].unique().tolist()),
        key="dept_dashboard"
    )

    dept_users = users[users["Department"] == dept]
    st.subheader(f"Team Members – {dept}")
    st.dataframe(dept_users, use_container_width=True)

    dept_tasks = tasks[tasks["Department"] == dept]
    st.subheader(f"Tasks – {dept}")
    st.dataframe(dept_tasks, use_container_width=True)

# ============================================================
# TAB 5 — ADD TASK
# ============================================================

with tab5:
    st.header("➕ Add New MoM Task")

    title = st.text_input("Task Title")
    details = st.text_area("Task Details")
    meeting_id = st.number_input("Meeting ID", min_value=1, step=1)
    department = st.selectbox("Assign to Department", sorted(users["Department"].unique().tolist()))
    assigned_name = st.selectbox("Assign To (Executive/Manager)", users["Name"])
    deadline = st.date_input("Deadline", value=date.today())
    created_by = 1  # You can map this to a user later

    if st.button("Create Task", key="create_task_btn"):
        try:
            assigned_id = int(users[users["Name"] == assigned_name]["UserID"].iloc[0])
            add_task(
                meeting_id=int(meeting_id),
                title=title,
                details=details,
                department=department,
                assigned_to=assigned_id,
                created_by=created_by,
                deadline=deadline
            )
            st.success("✅ Task added successfully!")
        except Exception as e:
            st.error(f"Error while adding task: {e}")

# ============================================================
# TAB 6 — ESCALATIONS
# ============================================================

with tab6:
    st.header("🚨 Escalation Log")
    st.dataframe(esc, use_container_width=True)

# ============================================================
# TAB 7 — AI MoM EXTRACTOR
# ============================================================

import openai
openai.api_key = os.getenv("OPENAI_API_KEY")

with tab7:
    st.header("🤖 AI MoM Extractor")
    st.write("Paste raw meeting notes below and let the agent extract tasks:")

    raw_notes = st.text_area("Meeting Notes", height=250, key="mom_raw_notes")

    if st.button("Extract Tasks with AI", key="extract_ai_btn"):
        if not raw_notes.strip():
            st.warning("Please paste some meeting notes first.")
        else:
            prompt = f"""
            Extract actionable MoM tasks from the following text.

            Output a valid JSON list of objects with fields:
            - title
            - details
            - department
            - assigned_to   (person name exactly as in the notes, or 'Unknown')
            - deadline      (YYYY-MM-DD or blank)

            Meeting Notes:
            {raw_notes}
            """

            try:
                resp = openai.ChatCompletion.create(
                    model=config["ai"]["model"],
                    messages=[{"role": "user", "content": prompt}]
                )
                extracted = resp["choices"][0]["message"]["content"]
                st.subheader("Extracted Tasks (Raw JSON Text)")
                st.code(extracted, language="json")
                st.session_state["ai_tasks_raw"] = extracted
            except Exception as e:
                st.error(f"Error from AI model: {e}")

    if "ai_tasks_raw" in st.session_state:
        st.markdown("### Save Extracted Tasks to MoM")
        if st.button("Save Extracted Tasks", key="save_ai_tasks_btn"):
            try:
                tasks_json = eval(st.session_state["ai_tasks_raw"])  # assuming trusted for now
                created_by = 1  # you

                for t in tasks_json:
                    assignee_name = t.get("assigned_to", "Unknown")
                    # If name exists in Users, map to ID, else skip
                    if assignee_name in users["Name"].values:
                        assigned_id = int(users[users["Name"] == assignee_name]["UserID"].iloc[0])
                    else:
                        # Default to your UserID if not found
                        assigned_id = int(users.iloc[0]["UserID"])

                    deadline_str = t.get("deadline")
                    if deadline_str:
                        try:
                            deadline_val = datetime.strptime(deadline_str, "%Y-%m-%d").date()
                        except Exception:
                            deadline_val = date.today()
                    else:
                        deadline_val = date.today()

                    add_task(
                        meeting_id=999,  # special AI-extracted MoM
                        title=t.get("title", ""),
                        details=t.get("details", ""),
                        department=t.get("department", ""),
                        assigned_to=assigned_id,
                        created_by=created_by,
                        deadline=deadline_val
                    )

                st.success("✅ Extracted tasks saved into MoM successfully!")
            except Exception as e:
                st.error(f"Error while saving extracted tasks: {e}")

# ============================================================
# TAB 8 — EXECUTIVE DASHBOARD
# ============================================================

with tab8:
    st.header("👤 Executive Dashboard")

    executive_name = st.selectbox("Select Executive", users["Name"], key="exec_sel_tab8")
    user_id = int(users[users["Name"] == executive_name]["UserID"].iloc[0])

    my_tasks = tasks[tasks["AssignedTo"] == user_id]

    today = pd.to_datetime(date.today())
    col1, col2, col3 = st.columns(3)
    col1.metric("Assigned Tasks", len(my_tasks))
    col2.metric("Completed", len(my_tasks[my_tasks["Status"] == "completed"]))
    col3.metric(
        "Overdue",
        len(my_tasks[(my_tasks["Deadline"] < today) & (my_tasks["Status"] == "pending")])
    )

    st.subheader("My Pending Tasks")
    st.dataframe(my_tasks[my_tasks["Status"] == "pending"], use_container_width=True)

# ============================================================
# TAB 9 — MANAGER DASHBOARD
# ============================================================

with tab9:
    st.header("🧑‍💼 Manager Dashboard")

    manager_name = st.selectbox("Select Manager", users["Name"], key="mgr_sel_tab9")
    manager_id = int(users[users["Name"] == manager_name]["UserID"].iloc[0])
    manager_dept = users[users["UserID"] == manager_id]["Department"].iloc[0]

    dept_users = users[users["Department"] == manager_dept]
    dept_user_ids = dept_users["UserID"].tolist()
    dept_tasks = tasks[tasks["AssignedTo"].isin(dept_user_ids)]

    today = pd.to_datetime(date.today())
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Team Size", len(dept_users))
    col2.metric("Team Tasks", len(dept_tasks))
    col3.metric("Completed", len(dept_tasks[dept_tasks["Status"] == "completed"]))
    col4.metric(
        "Overdue",
        len(dept_tasks[(dept_tasks["Deadline"] < today) & (dept_tasks["Status"] == "pending")])
    )

    st.subheader(f"{manager_dept} – Task Table")
    st.dataframe(dept_tasks, use_container_width=True)

# ============================================================
# TAB 10 — PERFORMANCE SCORECARD + PDFs
# ============================================================

with tab10:
    st.header("📈 Executive MoM Scorecard")

    today = pd.to_datetime(date.today())
    scores = []

    for _, user_row in users.iterrows():
        uid = user_row["UserID"]
        name = user_row["Name"]

        user_tasks = tasks[tasks["AssignedTo"] == uid]
        if len(user_tasks) == 0:
            continue

        completion_rate = (
            len(user_tasks[user_tasks["Status"] == "completed"]) / len(user_tasks) * 100
        )
        overdue_count = len(
            user_tasks[(user_tasks["Deadline"] < today) & (user_tasks["Status"] == "pending")]
        )
        score = round(max(0, 100 - overdue_count * 5) * (completion_rate / 100), 2)

        scores.append({
            "Name": name,
            "Department": user_row["Department"],
            "Score": score,
            "Tasks": len(user_tasks),
            "Overdue": overdue_count
        })

    st.dataframe(pd.DataFrame(scores), use_container_width=True)

    st.markdown("---")

    # ---- User Performance PDF ----
    st.subheader("📄 Download User Performance Score PDF")
    user_name_pdf = st.selectbox("Select Executive", users["Name"], key="pdf_exec_sel")
    if st.button("Generate User Score PDF", key="pdf_exec_btn"):
        pdf_path = generate_user_score_pdf(user_name_pdf)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download User Score PDF",
                data=f,
                mime="application/pdf",
                file_name="UserScore.pdf",
                key="pdf_exec_dl"
            )

    # ---- Department Summary PDF ----
    st.subheader("📄 Download Department Summary PDF")
    dept_name_pdf = st.selectbox(
        "Select Department",
        sorted(users["Department"].unique().tolist()),
        key="pdf_dept_sel"
    )
    if st.button("Generate Department PDF", key="pdf_dept_btn"):
        pdf_path = generate_department_summary(dept_name_pdf)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Department PDF",
                data=f,
                mime="application/pdf",
                file_name="DepartmentSummary.pdf",
                key="pdf_dept_dl"
            )

    # ---- Monthly Summary PDF (optional) ----
    st.subheader("🗓 Monthly Summary PDF")
    month_year = st.date_input("Select month (any date in month)", value=date.today())
    if st.button("Generate Monthly Summary PDF", key="pdf_monthly_btn"):
        pdf_path = generate_monthly_pdf(month_year.year, month_year.month)
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📥 Download Monthly Summary PDF",
                data=f,
                mime="application/pdf",
                file_name=f"MoM_Monthly_{month_year.year}_{month_year.month}.pdf",
                key="pdf_monthly_dl"
            )
