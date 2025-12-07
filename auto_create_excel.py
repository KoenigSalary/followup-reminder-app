import pandas as pd
import os
from openpyxl import Workbook

# REQUIRED SHEETS & STRUCTURES
SHEETS = {
    "Users": [
        "UserID", "Name", "Email", "Department", "Role"
    ],
    "Tasks": [
        "TaskID", "MeetingID", "Title", "Details", "Department",
        "AssignedTo", "CreatedBy", "CreatedDate", "Deadline",
        "Status", "LastUpdateDate", "LastUpdateBy"
    ],
    "Meetings": [
        "MeetingID", "MeetingName", "Date"
    ],
    "Logs": [
        "LogID", "TaskID", "Action", "Timestamp", "Actor"
    ],
    "Escalations": [
        "EscID", "TaskID", "Level", "Timestamp", "Note"
    ]
}


def auto_create_excel(excel_path):
    """
    Creates the full MoM Excel file with all sheets and required columns
    if the file does not exist OR is missing sheets.
    """

    # If file does NOT exist → create from scratch
    if not os.path.exists(excel_path):
        print(f"Creating new MoM Excel at: {excel_path}")
        wb = Workbook()
        wb.remove(wb.active)  # Remove default sheet

        for sheet, columns in SHEETS.items():
            df = pd.DataFrame(columns=columns)
            df.to_excel(excel_path, sheet_name=sheet, index=False)

        print("✔ Excel file created successfully!")
        return

    # If file exists → ensure all sheets exist
    print("Excel file found. Checking structure...")

    xls = pd.ExcelFile(excel_path)
    existing_sheets = xls.sheet_names

    # Append missing sheets
    with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a", if_sheet_exists="new") as writer:
        for sheet, columns in SHEETS.items():
            if sheet not in existing_sheets:
                print(f"Adding missing sheet: {sheet}")
                df = pd.DataFrame(columns=columns)
                df.to_excel(writer, sheet_name=sheet, index=False)

    # Now check columns in each sheet and fix missing ones
    for sheet, required_cols in SHEETS.items():
        df = pd.read_excel(excel_path, sheet_name=sheet)

        # Strip column names
        df.columns = df.columns.str.strip()

        # Add missing columns
        for col in required_cols:
            if col not in df.columns:
                print(f"Fixing missing column: {col} in sheet: {sheet}")
                df[col] = ""

        # Save updated sheet
        with pd.ExcelWriter(excel_path, engine="openpyxl", mode="a",
                            if_sheet_exists="replace") as writer:
            df.to_excel(writer, sheet_name=sheet, index=False)

    print("✔ Excel structure verified and corrected!")