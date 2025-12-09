#!/bin/bash
# Quick script to check if tasks were saved

cd ~/Downloads/Agent/followup_reminder_app

echo "📋 Checking your saved tasks..."
echo "================================"
echo ""

if [ -f "MoM_Master.xlsx" ]; then
    echo "✅ Found: MoM_Master.xlsx"
    echo "📍 Location: $(pwd)/MoM_Master.xlsx"
    echo "📊 File size: $(ls -lh MoM_Master.xlsx | awk '{print $5}')"
    echo ""
    echo "🔍 To view tasks:"
    echo "  1. Open MoM_Master.xlsx in Excel/Numbers"
    echo "  2. Go to 'Tasks' sheet"
    echo "  3. Look for your 21 newly added tasks!"
    echo ""
    echo "💡 OR view in Streamlit Dashboard:"
    echo "  1. Click '🔄 Refresh Data' in sidebar"
    echo "  2. Go to Tab 2: '📝 All Tasks'"
    echo ""
    
    # Try to open the file
    echo "📂 Opening file..."
    open MoM_Master.xlsx 2>/dev/null || echo "   (Run 'open MoM_Master.xlsx' to view)"
else
    echo "❌ MoM_Master.xlsx not found!"
    echo "📍 Current directory: $(pwd)"
    echo ""
    echo "💡 Make sure you're in: ~/Downloads/Agent/followup_reminder_app"
fi

echo ""
echo "================================"
