from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import date
import pandas as pd
import yaml

# Load config
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
MOM_FILE = config["paths"]["mom_file"]


def load_data():
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    users = pd.read_excel(MOM_FILE, sheet_name="Users")
    return tasks, users


def generate_department_summary(dept_name, output="DepartmentSummary.pdf"):

    tasks, users = load_data()

    dept_users = users[users["Department"] == dept_name]
    dept_ids = dept_users["UserID"].tolist()

    dept_tasks = tasks[tasks["AssignedTo"].isin(dept_ids)]

    completed = dept_tasks[dept_tasks["Status"] == "completed"]
    pending = dept_tasks[dept_tasks["Status"] == "pending"]
    overdue = dept_tasks[(dept_tasks["Deadline"] < date.today()) & (dept_tasks["Status"] == "pending")]

    # PDF
    c = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    y = height - 50

    # Logo
    try:
        c.drawImage(ImageReader(logo_url), 230, y - 50, width=140)
    except:
        pass

    y -= 120

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width/2, y, f"{dept_name} – Department MoM Summary")
    y -= 40

    # Stats
    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Total Tasks: {len(dept_tasks)}")
    y -= 20
    c.drawString(40, y, f"Completed: {len(completed)}")
    y -= 20
    c.drawString(40, y, f"Pending: {len(pending)}")
    y -= 20
    c.drawString(40, y, f"Overdue: {len(overdue)}")
    y -= 40

    # Overdue section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#E34234"))
    c.drawString(40, y, f"🔥 Overdue Tasks:")
    y -= 20
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)

    for _, row in overdue.iterrows():
        c.drawString(50, y, f"- [{row['TaskID']}] {row['Title']} (Due: {row['Deadline']})")
        y -= 15
        if y < 80:
            c.showPage()
            y = height - 50

    c.save()
    return output