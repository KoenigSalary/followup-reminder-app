import streamlit as st
import pandas as pd
import os
from datetime import date, datetime
import yaml
from pdf_user_score import generate_user_score_pdf
from pdf_department_summary import generate_department_summary
from monthly_summary_pdf import generate_monthly_pdf
from PIL import Image

# Must be the very first Streamlit command
st.set_page_config(
    page_title="Koenig MoM Automation Dashboard",
    page_icon=None,  # you can set to logo_url after loading config if available
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load config after page config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
dashboard_title = config["branding"]["dashboard_title"]
MOM_FILE = config["paths"]["mom_file"]
EXPORT_FOLDER = config["paths"]["export_folder"]

# Theme & CSS
st.markdown("""<style> ... your CSS ... </style>""", unsafe_allow_html=True)

# Main header: logo above title
st.image(logo_url, width=160)
st.markdown(f"<h2 style='text-align:center; margin-top:10px;'>{dashboard_title}</h2>", unsafe_allow_html=True)
st.markdown("<hr style='border:1px solid #e34234'>", unsafe_allow_html=True)

# Sidebar content
st.sidebar.markdown("## 🤖 Koenig MoM Agent")
st.sidebar.markdown("""
✅ Track all MoM actions  
✅ Monitor overdue tasks  
✅ Generate performance reports  
✅ Auto-email summaries  
✅ Maintain full accountability  

  
📌 **Status:** Live & Active  
📊 **Mode:** Automation  
🛡 **Owner:** Koenig Automation  
""")

# Load sheets safely
def load_sheets():
    if not os.path.exists(MOM_FILE):
        st.error(f"Excel file not found at path: {MOM_FILE}")
        st.stop()
    users = pd.read_excel(MOM_FILE, sheet_name="Users")
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    meetings = pd.read_excel(MOM_FILE, sheet_name="Meetings")
    logs = pd.read_excel(MOM_FILE, sheet_name="Logs")
    esc = pd.read_excel(MOM_FILE, sheet_name="Escalations")

    for df in [users, tasks, meetings, logs, esc]:
        df.columns = df.columns.str.strip()

    # Convert deadlines to datetime if present
    if "Deadline" in tasks.columns:
        tasks["Deadline"] = pd.to_datetime(tasks["Deadline"], errors="coerce")

    return users, tasks, meetings, logs, esc

users, tasks, meetings, logs, esc = load_sheets()

# Tabs creation
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

# Example: For tab2 ensure unique key for selectbox
with tab2:
    st.header("📄 All Tasks")
    dept_filter = st.selectbox(
        "Filter by Department",
        ["All"] + sorted(users["Department"].dropna().unique().tolist()),
        key="tasks_dept_filter"
    )
    df = tasks.copy()
    if dept_filter != "All":
        df = df[df["Department"] == dept_filter]
    st.dataframe(df, use_container_width=True)

# Tab5: Add Task
with tab5:
    st.header("➕ Add New MoM Task")
    title = st.text_input("Task Title", key="add_title")
    details = st.text_area("Task Details", key="add_details")
    meeting_id = st.number_input("Meeting ID", min_value=1, key="add_meeting_id")
    department = st.selectbox("Assign to Department", users["Department"].dropna().unique().tolist(), key="add_dept")
    assigned_name = st.selectbox("Assign To", users["Name"].dropna().unique().tolist(), key="add_assigned")
    deadline = st.date_input("Deadline", key="add_deadline")

    if st.button("Create Task", key="add_task_btn"):
        assigned_id = int(users[users["Name"] == assigned_name]["UserID"].iloc[0])
        from mom_agent import add_task
        add_task(
            meeting_id=meeting_id,
            title=title,
            details=details,
            department=department,
            assigned_to=assigned_id,
            created_by=999,
            deadline=deadline
        )
        st.success("✅ Task added successfully!")
        # Optionally refresh
        users, tasks, meetings, logs, esc = load_sheets()

# Tab7: AI MoM Extractor
with tab7:
    st.header("🤖 AI MoM Extractor")
    raw_notes = st.text_area("Paste meeting notes here:", height=250, key="ai_notes")

    if st.button("Extract Tasks with AI", key="ai_extract_btn"):
        import openai
        openai.api_key = os.getenv("OPENAI_API_KEY")
        prompt = f"""
        Extract actionable MoM tasks from the following text.

        Output JSON array of objects with keys:
        - title
        - details
        - department
        - assigned_to
        - deadline (YYYY-MM-DD or blank)
        """
        response = openai.ChatCompletion.create(
            model=config["ai"]["model"],
            messages=[{"role": "user", "content": prompt + raw_notes}]
        )
        extracted = response["choices"][0]["message"]["content"]
        st.subheader("Extracted Tasks (Review & Save)")
        st.json(extracted)
        st.session_state["extracted_tasks"] = extracted

    if "extracted_tasks" in st.session_state:
        if st.button("Save Extracted Tasks", key="ai_save_btn"):
            tasks_json = eval(st.session_state["extracted_tasks"])
            for t in tasks_json:
                assigned_id = int(users[users["Name"] == t["assigned_to"]]["UserID"].iloc[0])
                from mom_agent import add_task
                add_task(
                    meeting_id=999,
                    title=t["title"],
                    details=t["details"],
                    department=t["department"],
                    assigned_to=assigned_id,
                    created_by=999,
                    deadline=t.get("deadline") or date.today()
                )
            st.success("✅ Extracted tasks saved!")
            users, tasks, meetings, logs, esc = load_sheets()


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

    st.markdown("### 📄 Download User Performance Score PDF")

    user_name = st.selectbox(
        "Select Executive",
        users["Name"],
        key="pdf_exec"
    )

    if st.button("Generate User Score PDF", key="pdf_exec_btn"):
        pdf_path = generate_user_score_pdf(user_name)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download User Performance Score PDF",
                f,
                file_name="UserScore.pdf",
                key="pdf_exec_dl"
            )

    st.markdown("---")

    st.markdown("### 📄 Download Department Summary PDF")

    dept_name = st.selectbox(
        "Select Department",
        users["Department"].unique(),
        key="pdf_dept"
    )

    if st.button("Generate Department PDF", key="pdf_dept_btn"):
        pdf_path = generate_department_summary(dept_name)
        with open(pdf_path, "rb") as f:
            st.download_button(
                "⬇️ Download Department Summary PDF",
                f,
                file_name="DepartmentSummary.pdf",
                key="pdf_dept_dl"
            )
