#!/usr/bin/env python3
"""
Test script to verify task saving works
"""

import sys
import os
os.chdir(os.path.expanduser('~/Downloads/Agent/followup_reminder_app'))

print("🧪 Testing task save functionality...")
print("=" * 60)
print()

# Import the fixed function
exec(open('FIXED_add_task_function.py').read())

# Test saving one task
print("📝 Attempting to save test task...")

try:
    result = add_task(
        meeting_id="TEST-001",
        title="Test Task - Follow up on Japan Entity",
        details="This is a test task to verify saving works",
        department="Finance",
        assigned_to="Aditya",
        created_by="AI-Agent",
        deadline="2024-01-15",
        category="Regular"
    )
    
    if result:
        print()
        print("=" * 60)
        print("✅ SUCCESS! Task saved successfully!")
        print("=" * 60)
        print()
        print("Now verify:")
        print("1. Open MoM_Master.xlsx")
        print("2. Go to Tasks sheet")
        print("3. Scroll to bottom - you should see task #4")
        print()
    else:
        print()
        print("❌ Save returned False - check errors above")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
