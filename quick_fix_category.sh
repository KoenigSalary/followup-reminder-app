#!/bin/bash
# Quick fix for Category column error in streamlit_app.py

echo "🔧 Fixing streamlit_app.py Category error..."

# Backup original
cp streamlit_app.py streamlit_app_backup_$(date +%Y%m%d_%H%M%S).py

# Create patched version
python3 << 'EOFPYTHON'
import re

# Read the file
with open('streamlit_app.py', 'r') as f:
    content = f.read()

# Fix 1: Add Category column check in load_data()
fix1_pattern = r"(escalations = pd\.read_excel\(MOM_FILE, sheet_name='Escalations'\))\s*(# Convert dates)"
fix1_replacement = r"\1\n        \n        # FIX: Add Category column if missing\n        if 'Category' not in tasks.columns:\n            tasks['Category'] = 'Regular'\n        \n        \2"
content = re.sub(fix1_pattern, fix1_replacement, content)

# Fix 2: Replace Boss-MoM tab direct access
fix2_pattern = r"boss_tasks = tasks\[tasks\['Category'\] == 'Boss-MoM'\]"
fix2_replacement = """# FIX: Handle missing Category column gracefully
    if 'Category' in tasks.columns:
        boss_tasks = tasks[tasks['Category'] == 'Boss-MoM']
    else:
        boss_tasks = tasks[tasks['Title'].str.contains('Boss', case=False, na=False)]
    
    if len(boss_tasks) > 0:
        st.dataframe(boss_tasks, use_container_width=True)
    else:
        st.info("ℹ️ No Boss-MoM tasks found")"""

content = re.sub(fix2_pattern, fix2_replacement, content)

# Write fixed version
with open('streamlit_app.py', 'w') as f:
    f.write(content)

print("✅ streamlit_app.py fixed!")
EOFPYTHON

echo ""
echo "✅ Fix applied!"
echo ""
echo "Run: streamlit run streamlit_app.py"
