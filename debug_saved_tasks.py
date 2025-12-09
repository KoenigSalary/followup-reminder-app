#!/usr/bin/env python3
"""
Debug script to check if tasks were saved to MoM_Master.xlsx
"""

import pandas as pd
import os
from datetime import datetime

print("=" * 60)
print("🔍 DEBUG: Checking Saved Tasks")
print("=" * 60)
print()

# Check if file exists
mom_file = "MoM_Master.xlsx"

if not os.path.exists(mom_file):
    print(f"❌ ERROR: {mom_file} not found!")
    print(f"📍 Current directory: {os.getcwd()}")
    print()
    print("💡 Make sure you're in the correct directory:")
    print("   cd ~/Downloads/Agent/followup_reminder_app")
    exit(1)

print(f"✅ Found: {mom_file}")
print(f"📍 Location: {os.path.abspath(mom_file)}")
print(f"📊 File size: {os.path.getsize(mom_file) / 1024:.1f} KB")
print()

# Read the Tasks sheet
try:
    df = pd.read_excel(mom_file, sheet_name='Tasks')
    
    print(f"📋 Total tasks in database: {len(df)}")
    print()
    
    # Show last 25 tasks (should include the AI-extracted ones)
    print("🔍 Last 25 tasks (most recent):")
    print("=" * 60)
    
    recent = df.tail(25)
    
    for idx, row in recent.iterrows():
        print(f"\n#{row.get('TaskID', 'N/A')} - {row.get('Title', 'No Title')}")
        print(f"   Assigned: {row.get('AssignedTo', 'N/A')}")
        print(f"   Department: {row.get('Department', 'N/A')}")
        print(f"   Status: {row.get('Status', 'N/A')}")
        print(f"   Created: {row.get('CreatedDate', 'N/A')}")
        if 'CreatedBy' in df.columns:
            print(f"   Created By: {row.get('CreatedBy', 'N/A')}")
    
    print()
    print("=" * 60)
    
    # Check for AI-Agent created tasks
    if 'CreatedBy' in df.columns:
        ai_tasks = df[df['CreatedBy'] == 'AI-Agent']
        print(f"\n🤖 AI-Agent created tasks: {len(ai_tasks)}")
        
        if len(ai_tasks) > 0:
            print("\n✅ AI-extracted tasks found:")
            for idx, row in ai_tasks.iterrows():
                print(f"  - {row.get('Title', 'No Title')} ({row.get('AssignedTo', 'N/A')})")
        else:
            print("\n⚠️ No tasks created by 'AI-Agent' found")
            print("💡 This means the save might have failed")
    else:
        print("\n⚠️ 'CreatedBy' column not found in Tasks sheet")
    
    # Check today's tasks
    if 'CreatedDate' in df.columns:
        df['CreatedDate'] = pd.to_datetime(df['CreatedDate'], errors='coerce')
        today = datetime.now().date()
        today_tasks = df[df['CreatedDate'].dt.date == today]
        
        print(f"\n📅 Tasks created today: {len(today_tasks)}")
        
        if len(today_tasks) > 0:
            print("\n✅ Today's new tasks:")
            for idx, row in today_tasks.iterrows():
                print(f"  - {row.get('Title', 'No Title')} ({row.get('AssignedTo', 'N/A')})")
    
    print()
    print("=" * 60)
    print("\n💡 NEXT STEPS:")
    print("1. If you see your 21 tasks above: ✅ They were saved!")
    print("2. In Streamlit: Click '🔄 Refresh Data' button")
    print("3. Go to Tab 2: '📝 All Tasks'")
    print("4. Scroll to bottom or filter by today's date")
    print()
    
except Exception as e:
    print(f"❌ ERROR reading Tasks sheet: {e}")
    print()
    print("💡 Try opening MoM_Master.xlsx in Excel/Numbers")
    print("   and check the 'Tasks' sheet manually")
