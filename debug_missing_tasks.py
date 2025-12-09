#!/usr/bin/env python3
"""
Debug script to find why saved tasks aren't appearing
"""

import pandas as pd
import os
from datetime import datetime
import sys

print("=" * 70)
print("🔍 DEBUGGING: Why Saved Tasks Aren't Showing")
print("=" * 70)
print()

# Change to the correct directory
os.chdir(os.path.expanduser('~/Downloads/Agent/followup_reminder_app'))
print(f"📍 Working directory: {os.getcwd()}")
print()

mom_file = "MoM_Master.xlsx"

if not os.path.exists(mom_file):
    print(f"❌ ERROR: {mom_file} not found!")
    print(f"📍 Looking in: {os.getcwd()}")
    sys.exit(1)

print(f"✅ Found: {mom_file}")
print(f"📊 File size: {os.path.getsize(mom_file) / 1024:.1f} KB")
print(f"📅 Last modified: {datetime.fromtimestamp(os.path.getmtime(mom_file))}")
print()

# Read the Tasks sheet
try:
    print("📖 Reading Tasks sheet...")
    df = pd.read_excel(mom_file, sheet_name='Tasks')
    
    print(f"✅ Loaded {len(df)} total tasks")
    print()
    
    # Show columns
    print("📋 Columns in Tasks sheet:")
    for col in df.columns:
        print(f"  - {col}")
    print()
    
    # Check for recent tasks
    print("=" * 70)
    print("🔍 ANALYSIS:")
    print("=" * 70)
    print()
    
    # 1. Show last 10 tasks
    print("📌 Last 10 tasks (most recent):")
    print("-" * 70)
    recent = df.tail(10)
    for idx, row in recent.iterrows():
        task_id = row.get('TaskID', 'N/A')
        title = row.get('Title', 'No Title')[:50]
        assigned = row.get('AssignedTo', 'N/A')
        status = row.get('Status', 'N/A')
        created = row.get('CreatedDate', 'N/A')
        
        print(f"#{task_id} | {title}")
        print(f"   → Assigned: {assigned} | Status: {status}")
        print(f"   → Created: {created}")
        print()
    
    # 2. Check for AI-Agent tasks
    print("-" * 70)
    if 'CreatedBy' in df.columns:
        ai_tasks = df[df['CreatedBy'] == 'AI-Agent']
        print(f"🤖 Tasks created by 'AI-Agent': {len(ai_tasks)}")
        
        if len(ai_tasks) > 0:
            print("\n✅ AI-extracted tasks found:")
            for idx, row in ai_tasks.tail(10).iterrows():
                print(f"  - #{row.get('TaskID')} {row.get('Title', 'No Title')[:50]}")
        else:
            print("\n❌ No AI-Agent tasks found!")
            print("💡 This means the 'Save All Tasks' button didn't actually save them")
    else:
        print("⚠️ 'CreatedBy' column doesn't exist")
    
    print()
    
    # 3. Check today's tasks
    print("-" * 70)
    if 'CreatedDate' in df.columns:
        df['CreatedDate'] = pd.to_datetime(df['CreatedDate'], errors='coerce')
        today = datetime.now().date()
        today_tasks = df[df['CreatedDate'].dt.date == today]
        
        print(f"📅 Tasks created TODAY ({today}): {len(today_tasks)}")
        
        if len(today_tasks) > 0:
            print("\n✅ Today's tasks:")
            for idx, row in today_tasks.iterrows():
                print(f"  - #{row.get('TaskID')} {row.get('Title', 'No Title')[:50]}")
                print(f"    Assigned: {row.get('AssignedTo')} | Created: {row.get('CreatedDate')}")
        else:
            print("\n❌ No tasks created today!")
            print("💡 The save didn't work - we need to fix the save button")
    
    print()
    
    # 4. Status breakdown
    print("-" * 70)
    print("📊 Tasks by Status:")
    if 'Status' in df.columns:
        status_counts = df['Status'].value_counts()
        for status, count in status_counts.items():
            print(f"  - {status}: {count}")
    
    print()
    
    # 5. Check for specific names from your meeting notes
    print("-" * 70)
    print("🔍 Checking for tasks assigned to team members:")
    team_members = ['Aditya', 'Sarika', 'Sunil', 'Anurag', 'Ajay', 'Jatin']
    
    if 'AssignedTo' in df.columns:
        for member in team_members:
            member_tasks = df[df['AssignedTo'].astype(str).str.contains(member, case=False, na=False)]
            print(f"  - {member}: {len(member_tasks)} task(s)")
    
    print()
    print("=" * 70)
    print("💡 CONCLUSION:")
    print("=" * 70)
    print()
    
    if len(ai_tasks) == 0 and len(today_tasks) == 0:
        print("❌ ISSUE FOUND: No tasks were actually saved!")
        print()
        print("🔧 REASON: The 'Save All Tasks' button has a bug")
        print()
        print("✅ SOLUTION: We need to fix the save button in Tab 7")
        print("   I'll provide the fixed code now.")
    else:
        print("✅ Tasks ARE in the database!")
        print()
        print("🔧 ISSUE: Dashboard cache isn't refreshing properly")
        print()
        print("✅ SOLUTION:")
        print("   1. In Streamlit, click '🔄 Refresh Data' button")
        print("   2. Go to Tab 2: 'All Tasks'")
        print("   3. Clear all filters, then reapply them")
        print("   4. Scroll to the very bottom of the table")
    
    print()
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
