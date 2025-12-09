#!/bin/bash
# Quick fix for .str accessor error

cd ~/Downloads/Agent/followup_reminder_app

echo "🔧 Fixing .str accessor errors..."

# Backup
cp streamlit_app.py streamlit_app_backup_$(date +%Y%m%d_%H%M%S).py

# Apply fixes using sed
sed -i.bak "s/tasks\['AssignedTo'\]\.str\.contains/tasks['AssignedTo'].astype(str).str.contains/g" streamlit_app.py
sed -i.bak "s/tasks\['Title'\]\.str\.contains/tasks['Title'].astype(str).str.contains/g" streamlit_app.py

echo "✅ Fixed!"
echo ""
echo "Run: streamlit run streamlit_app.py"
