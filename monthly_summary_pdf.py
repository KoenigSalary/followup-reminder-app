import pandas as pd
from datetime import date, datetime
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
import matplotlib.pyplot as plt
import yaml
import os

# ---------------------------------------------------------
# Load config
# ---------------------------------------------------------
base_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(base_dir, "config.yaml")

with open(config_path, "r") as f:
    config = yaml.safe_load(f)

logo_url = config["branding"]["logo_url"]
MOM_FILE = config["paths"]["mom_file"]


# ---------------------------------------------------------
# Load Excel data
# ---------------------------------------------------------
def load_data():
    tasks = pd.read_excel(MOM_FILE, sheet_name="Tasks")
    users = pd.read_excel(MOM_FILE, sheet_name="Users")

    # Strip column names
    tasks.columns = tasks.columns.str.strip()
    users.columns = users.columns.str.strip()

    return tasks, users


# ---------------------------------------------------------
# Get month start → today date range
# ---------------------------------------------------------
def get_month_range():
    today = date.today()
    start = date(today.year, today.month, 1)
    return start, today


# ---------------------------------------------------------
# Draw section title
# ---------------------------------------------------------
def section_title(c, text, y):
    c.setFont("Helvetica-Bold", 15)
    c.setFillColor(colors.HexColor("#E34234"))
    c.drawString(40, y, text)
    return y - 25


# ---------------------------------------------------------
# Draw chart and insert into PDF
# ---------------------------------------------------------
def add_chart_to_pdf(c, chart_path, y):
    c.drawImage(chart_path, 50, y - 180, width=500, height=180)
    return y - 200


# ---------------------------------------------------------
# MAIN PDF GENERATOR
# ---------------------------------------------------------
def generate_monthly_pdf(output="Monthly_MoM_Summary.pdf"):

    tasks, users = load_data()
    start, today = get_month_range()

    # Filter tasks for this month
    monthly = tasks[(tasks["CreatedDate"] >= pd.to_datetime(start)) &
                    (tasks["CreatedDate"] <= pd.to_datetime(today))]

    completed = monthly[monthly["Status"] == "completed"]
    pending = monthly[monthly["Status"] == "pending"]
    overdue = monthly[(monthly["Status"] == "pending") &
                      (monthly["Deadline"] < pd.to_datetime(today))]

    # -----------------------------------------------------
    # Create PDF
    # -----------------------------------------------------
    c = canvas.Canvas(output, pagesize=A4)
    width, height = A4
    y = height - 50

    # Logo
    try:
        logo = ImageReader(logo_url)
        c.drawImage(logo, 240, y - 60, width=120)
    except:
        pass

    y -= 120

    # Title
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, y, "Monthly MoM Summary Report")
    y -= 30

    c.setFont("Helvetica", 12)
    c.drawCentredString(width / 2, y, f"Period: {start} to {today}")
    y -= 40

    # -----------------------------------------------------
    # TASK COUNTS
    # -----------------------------------------------------
    y = section_title(c, "📌 Summary Counts", y)

    c.setFont("Helvetica", 12)
    c.setFillColor(colors.black)
    c.drawString(50, y, f"Total tasks created this month: {len(monthly)}")
    y -= 20
    c.drawString(50, y, f"Completed: {len(completed)}")
    y -= 20
    c.drawString(50, y, f"Pending: {len(pending)}")
    y -= 20
    c.drawString(50, y, f"Overdue: {len(overdue)}")
    y -= 40

    # -----------------------------------------------------
    # CHART 1 — Completed vs Pending vs Overdue
    # -----------------------------------------------------
    chart1 = "chart_status.png"
    plt.figure(figsize=(5, 3))
    plt.bar(["Completed", "Pending", "Overdue"], [len(completed), len(pending), len(overdue)])
    plt.title("Task Status Breakdown")
    plt.savefig(chart1, bbox_inches="tight")
    plt.close()

    y = add_chart_to_pdf(c, chart1, y)

    # -----------------------------------------------------
    # CHART 2 — Department Summary
    # -----------------------------------------------------
    dept_summary = monthly.groupby("Department").size()
    chart2 = "chart_dept.png"
    plt.figure(figsize=(5, 3))
    dept_summary.plot(kind='bar')
    plt.title("Tasks by Department")
    plt.tight_layout()
    plt.savefig(chart2)
    plt.close()

    y = add_chart_to_pdf(c, chart2, y)

    # Save PDF
    c.save()
    return output