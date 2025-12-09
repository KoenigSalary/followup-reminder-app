#!/usr/bin/env python3
"""
COMPREHENSIVE DIAGNOSTIC: Why is add_task() failing?
This script will pinpoint the exact problem.
"""

import os
import sys
from pathlib import Path

print("=" * 70)
print("🔍 DIAGNOSING SAVE FAILURE")
print("=" * 70)

# Step 1: Check if we're in the right directory
print("\n📁 Step 1: Check Current Directory")
print(f"Current directory: {os.getcwd()}")
expected_dir = Path.home() / "Downloads/Agent/followup_reminder_app"
print(f"Expected directory: {expected_dir}")
print(f"✅ Directory exists: {expected_dir.exists()}")

# Step 2: Check if mom_agent.py exists
print("\n📄 Step 2: Check mom_agent.py")
mom_agent_path = Path("mom_agent.py")
if mom_agent_path.exists():
    print(f"✅ mom_agent.py found: {mom_agent_path.absolute()}")
    file_size = mom_agent_path.stat().st_size
    print(f"   File size: {file_size} bytes")
else:
    print("❌ mom_agent.py NOT FOUND!")
    sys.exit(1)

# Step 3: Check if MoM_Master.xlsx exists
print("\n📊 Step 3: Check MoM_Master.xlsx")
excel_path = Path("MoM_Master.xlsx")
if excel_path.exists():
    print(f"✅ MoM_Master.xlsx found: {excel_path.absolute()}")
    file_size = excel_path.stat().st_size
    print(f"   File size: {file_size} bytes")
    
    # Check if file is writable
    if os.access(excel_path, os.W_OK):
        print("✅ File is writable")
    else:
        print("❌ File is NOT writable (permission issue)")
else:
    print("❌ MoM_Master.xlsx NOT FOUND!")
    sys.exit(1)

# Step 4: Try to import mom_agent
print("\n📦 Step 4: Import mom_agent module")
try:
    import mom_agent
    print("✅ mom_agent imported successfully")
except Exception as e:
    print(f"❌ Failed to import mom_agent: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Step 5: Check if add_task function exists
print("\n🔧 Step 5: Check add_task function")
if hasattr(mom_agent, 'add_task'):
    print("✅ add_task function exists")
    
    # Check function signature
    import inspect
    sig = inspect.signature(mom_agent.add_task)
    print(f"   Function signature: add_task{sig}")
    
    params = list(sig.parameters.keys())
    print(f"   Parameters: {params}")
    
    if 'category' in params:
        print("✅ 'category' parameter EXISTS in function")
    else:
        print("❌ 'category' parameter MISSING from function!")
        print("   → This is the problem! Update mom_agent.py to include 'category' parameter")
else:
    print("❌ add_task function NOT FOUND in mom_agent!")
    sys.exit(1)

# Step 6: Check required libraries
print("\n📚 Step 6: Check Required Libraries")
libraries = ['pandas', 'openpyxl', 'yaml']
for lib in libraries:
    try:
        __import__(lib)
        print(f"✅ {lib} is installed")
    except ImportError:
        print(f"❌ {lib} is NOT installed")
        print(f"   Install with: pip install {lib}")

# Step 7: Try to read Excel file
print("\n📖 Step 7: Try Reading Excel File")
try:
    import pandas as pd
    df = pd.read_excel('MoM_Master.xlsx', sheet_name='Tasks')
    print(f"✅ Successfully read Excel file")
    print(f"   Current tasks: {len(df)}")
    print(f"   Columns: {list(df.columns)}")
    
    if 'Category' in df.columns:
        print("✅ 'Category' column exists in Excel")
    else:
        print("⚠️  'Category' column MISSING from Excel - will be added automatically")
except Exception as e:
    print(f"❌ Failed to read Excel: {e}")
    import traceback
    traceback.print_exc()

# Step 8: Attempt to save a test task
print("\n💾 Step 8: Attempt to Save Test Task")
try:
    from datetime import datetime, timedelta
    
    deadline = datetime.now() + timedelta(days=7)
    
    print("Calling add_task with parameters:")
    print(f"  title='DIAGNOSTIC TEST'")
    print(f"  details='Testing save function'")
    print(f"  department='IT'")
    print(f"  assigned_to='Test User'")
    print(f"  created_by='Diagnostic Script'")
    print(f"  deadline={deadline}")
    print(f"  meeting_id=''")
    print(f"  category='Regular'")
    
    task_id = mom_agent.add_task(
        title="DIAGNOSTIC TEST",
        details="Testing save function",
        department="IT",
        assigned_to="Test User",
        created_by="Diagnostic Script",
        deadline=deadline,
        meeting_id='',
        category='Regular'
    )
    
    print(f"\n✅ SUCCESS! Task saved with ID: {task_id}")
    
    # Verify task was actually saved
    df = pd.read_excel('MoM_Master.xlsx', sheet_name='Tasks')
    if task_id in df['TaskID'].values:
        print(f"✅ VERIFIED: Task #{task_id} appears in Excel file")
        print("\n🎉 THE SAVE FUNCTION IS WORKING!")
    else:
        print(f"❌ WARNING: Task #{task_id} NOT found in Excel after save")
        print("   The function returned success but didn't actually save")
        
except TypeError as e:
    print(f"\n❌ FAILED: TypeError (parameter mismatch)")
    print(f"   Error: {e}")
    print("\n   → SOLUTION: The function signature doesn't match the parameters")
    print("   → Update mom_agent.py to accept 'category' parameter")
    import traceback
    traceback.print_exc()
    
except Exception as e:
    print(f"\n❌ FAILED: {type(e).__name__}")
    print(f"   Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
print("🏁 DIAGNOSTIC COMPLETE")
print("=" * 70)
