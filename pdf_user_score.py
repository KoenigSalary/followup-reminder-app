from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import date
import pandas as pd
import yaml

# ---------------------------------------------------------
# Load Configuration
# ---------------------------------------------------------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
MOM_FILE = config["paths"]["mom_file"]


# ---------------------------------------------------------
# Load Data
# ---------------------------------------------------------
def load_data():
    users = pd.read_excel(MOM_FILE, sheet_name="Users")
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    return users, tasks


# ---------------------------------------------------------
# Generate User Score PDF
# ---------------------------------------------------------
def generate_user_score_pdf(user_name, output="UserScore.pdf"):

    users, tasks = load_data()
    width, height = A4
    c = canvas.Canvas(output, pagesize=A4)

    # Get user record
    user = users[users["Name"] == user_name].iloc[0]
    user_id = int(user["UserID"])
    dept = user["Department"]

    # Get user tasks
    my_tasks = tasks[tasks["AssignedTo"] == user_id]
    completed = my_tasks[my_tasks["Status"] == "completed"]
    pending = my_tasks[my_tasks["Status"] == "pending"]
    overdue = my_tasks[(my_tasks["Deadline"] < date.today()) & (my_tasks["Status"] == "pending")]

    # Compute score
    if len(my_tasks) > 0:
        completion_rate = len(completed) / len(my_tasks) * 100
        score = max(0, 100 - len(overdue) * 5) * (completion_rate / 100)
    else:
        completion_rate = 0
        score = 0

    # PDF Layout
    y = height - 50

    # Logo
    try:
        c.drawImage(ImageReader(logo_url), 230, y - 50, width=140)
    except:
        pass

    y -= 120

    # Title
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y, f"User Performance Score Report")
    y -= 20
    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, y, f"Executive: {user_name} | Department: {dept}")
    y -= 40

    # Score Section
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#E34234"))
    c.drawString(40, y, f"Performance Score: {round(score,2)} / 100")
    y -= 30

    # Task Stats
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 12)
    c.drawString(40, y, f"Total Tasks Assigned: {len(my_tasks)}")
    y -= 20
    c.drawString(40, y, f"Completed Tasks: {len(completed)}")
    y -= 20
    c.drawString(40, y, f"Pending Tasks: {len(pending)}")
    y -= 20
    c.drawString(40, y, f"Overdue Tasks: {len(overdue)}")
    y -= 40

    # Overdue details
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#E34234"))
    c.drawString(40, y, "Overdue Task Details:")
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