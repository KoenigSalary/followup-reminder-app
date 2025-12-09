#!/bin/bash
# Auto-fix .str accessor errors in streamlit_app.py

cd ~/Downloads/Agent/followup_reminder_app

echo "🔧 Fixing .str accessor errors..."

# Backup first
cp streamlit_app.py streamlit_app_backup_$(date +%Y%m%d_%H%M%S).py

# Fix all .str accessor issues
python3 << 'EOFPYTHON'
# Read file
with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Fix 1: Tab 8 - Executive
content = content.replace(
    "tasks[tasks['AssignedTo'].str.contains('Executive', case=False, na=False)]",
    "tasks[tasks['AssignedTo'].astype(str).str.contains('Executive', case=False, na=False)]"
)

# Fix 2: Tab 9 - Manager
content = content.replace(
    "tasks[tasks['AssignedTo'].str.contains('Manager', case=False, na=False)]",
    "tasks[tasks['AssignedTo'].astype(str).str.contains('Manager', case=False, na=False)]"
)

# Fix 3: Tab 3 - Boss-MoM (Title column)
content = content.replace(
    "tasks[tasks['Title'].str.contains('Boss', case=False, na=False)]",
    "tasks[tasks['Title'].astype(str).str.contains('Boss', case=False, na=False)]"
)

# Write back
with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("✅ All .str accessor errors fixed!")
EOFPYTHON

echo ""
echo "✅ Fix complete!"
echo ""
echo "Run: streamlit run streamlit_app.py"
