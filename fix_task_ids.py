import pandas as pd
import uuid

file_path = "MoM_Master.xlsx"

# Load Tasks sheet
df = pd.read_excel(file_path, sheet_name="Tasks")

# ✅ Fix TaskID
df["TaskID"] = [
    f"TASK-{uuid.uuid4().hex[:8].upper()}" for _ in range(len(df))
]

# ✅ Fix MeetingID where it is AI-Extract
df["MeetingID"] = [
    f"AI-FIXED-{i+1}" if str(x).strip() == "AI-Extract" else x
    for i, x in enumerate(df["MeetingID"])
]

# Save back to Excel
df.to_excel(file_path, sheet_name="Tasks", index=False)

print("✅ TaskID and MeetingID fixed successfully!")

