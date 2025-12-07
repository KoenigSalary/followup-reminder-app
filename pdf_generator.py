from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from datetime import date
import pandas as pd
import yaml

# ---------------------------------------------------------
# Load config
# ---------------------------------------------------------
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
MOM_FILE = config["paths"]["mom_file"]

# ---------------------------------------------------------
# Load data from Excel
# ---------------------------------------------------------
def load_data():
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    users = pd.read_excel(MOM_FILE, sheet_name="Users")
    return tasks, users

# ---------------------------------------------------------
# Draw section title
# ---------------------------------------------------------
def section_title(c, title, y):
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(colors.HexColor("#E34234"))  # Koenig Red
    c.drawString(40, y, title)
    return y - 20

# ---------------------------------------------------------
# Draw bullet list of tasks
# ---------------------------------------------------------
def draw_tasks(c, data, y):
    c.setFont("Helvetica", 11)
    c.setFillColor(colors.black)

    for _, row in data.iterrows():
        text = f"- [{row['TaskID']}] {row['Title']}  (Due: {row['Deadline']})"
        c.drawString(50, y, text)
        y -= 15
        if y < 80:  # New page
            c.showPage()
            y = 800

    return y

# ---------------------------------------------------------
# MAIN PDF GENERATOR
# ---------------------------------------------------------
def generate_mom_pdf(output_path="MoM_Summary.pdf"):
    tasks, users = load_data()

    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 50

    # -----------------------------------------------------
    # LOGO
    # -----------------------------------------------------
    try:
        logo = ImageReader(logo_url)
        c.drawImage(logo, 230, y - 50, width=140, preserveAspectRatio=True)
    except:
        pass

    y -= 120

    # -----------------------------------------------------
    # TITLE
    # -----------------------------------------------------
    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(width / 2, y, "Koenig – MoM Summary Report")
    y -= 20

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, y, f"Date: {date.today()}")
    y -= 40

    # -----------------------------------------------------
    # Completed Tasks
    # -----------------------------------------------------
    completed = tasks[tasks["Status"] == "completed"]
    y = section_title(c, "✔ Completed Tasks", y)
    y = draw_tasks(c, completed, y - 10)

    # -----------------------------------------------------
    # Pending Tasks
    # -----------------------------------------------------
    pending = tasks[tasks["Status"] == "pending"]
    y = section_title(c, "⏳ Pending Tasks", y)
    y = draw_tasks(c, pending, y - 10)

    # -----------------------------------------------------
    # Overdue Tasks
    # -----------------------------------------------------
    overdue = tasks[(tasks["Status"] != "completed") & (tasks["Deadline"] < date.today())]
    y = section_title(c, "🔥 Overdue Tasks", y)
    y = draw_tasks(c, overdue, y - 10)

    # -----------------------------------------------------
    # Boss-MoM Tasks
    # -----------------------------------------------------
    boss_id = config["meetings"]["boss_meeting_id"]
    boss_tasks = tasks[tasks["MeetingID"] == boss_id]

    y = section_title(c, "⭐ Boss-MoM Action Items", y)
    y = draw_tasks(c, boss_tasks, y - 10)

    # -----------------------------------------------------
    # SAVE PDF
    # -----------------------------------------------------
    c.save()
    return output_path