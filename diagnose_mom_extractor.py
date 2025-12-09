#!/usr/bin/env python3
"""
DIAGNOSE: Why is AI MoM Extractor failing to save tasks?
"""

import json

# This is the sample JSON output from earlier that you showed me
sample_json = """
[
  {
    "title": "Finalize Q4 Marketing Budget",
    "details": "Review and approve the final Q4 marketing budget, ensuring alignment with company goals.",
    "assigned_to": "Rajesh Kumar",
    "department": "Marketing",
    "deadline": "2025-12-15"
  },
  {
    "title": "Complete Cybersecurity Audit",
    "details": "Conduct a comprehensive cybersecurity audit for all company systems and networks.",
    "assigned_to": "Priya Sharma",
    "department": "IT",
    "deadline": "2025-12-20"
  }
]
"""

print("=" * 70)
print("🔍 DIAGNOSING AI MoM EXTRACTOR")
print("=" * 70)

# Test 1: Can we parse the JSON?
print("\n📝 Test 1: Parse JSON")
try:
    tasks = json.loads(sample_json)
    print(f"✅ JSON parsed successfully")
    print(f"   Tasks extracted: {len(tasks)}")
    print(f"   First task title: {tasks[0]['title']}")
except json.JSONDecodeError as e:
    print(f"❌ JSON parsing failed: {e}")

# Test 2: Check if JSON has markdown fence
print("\n📝 Test 2: Check for Markdown Fence")
if sample_json.strip().startswith('```'):
    print("⚠️  JSON is wrapped in markdown code blocks!")
    print("   This will cause parsing to fail")
    
    # Strip markdown
    cleaned = sample_json.strip()
    if cleaned.startswith('```json'):
        cleaned = cleaned[7:]  # Remove ```json
    elif cleaned.startswith('```'):
        cleaned = cleaned[3:]   # Remove ```
    
    if cleaned.endswith('```'):
        cleaned = cleaned[:-3]  # Remove trailing ```
    
    cleaned = cleaned.strip()
    print("\n   Cleaned JSON (first 100 chars):")
    print(f"   {cleaned[:100]}...")
    
    try:
        tasks = json.loads(cleaned)
        print(f"\n✅ After cleaning: {len(tasks)} tasks parsed")
    except:
        print(f"\n❌ Still failed after cleaning")
else:
    print("✅ JSON is clean (no markdown fence)")

# Test 3: Check required fields
print("\n📝 Test 3: Check Required Fields")
required_fields = ['title', 'details', 'assigned_to', 'department', 'deadline']

try:
    tasks = json.loads(sample_json)
    for i, task in enumerate(tasks):
        print(f"\nTask {i+1}: {task.get('title', 'NO TITLE')}")
        for field in required_fields:
            if field in task:
                print(f"  ✅ {field}: {task[field]}")
            else:
                print(f"  ❌ MISSING: {field}")
except Exception as e:
    print(f"❌ Error: {e}")

# Test 4: Simulate the streamlit save process
print("\n📝 Test 4: Simulate Streamlit Save Process")
print("\nThis is what happens when you click 'Save All Tasks':\n")

try:
    import sys
    sys.path.insert(0, '/Users/praveenchaudhary/Downloads/Agent/followup_reminder_app')
    from mom_agent import add_task
    from datetime import datetime
    
    tasks = json.loads(sample_json)
    saved_count = 0
    failed_count = 0
    
    for task in tasks:
        try:
            # Convert deadline string to datetime
            deadline = datetime.strptime(task['deadline'], '%Y-%m-%d')
            
            # Call add_task - NOTE THE PARAMETER ORDER!
            task_id = add_task(
                meeting_id='',  # ← FIRST parameter
                title=task['title'],
                details=task['details'],
                department=task['department'],
                assigned_to=task['assigned_to'],
                created_by='AI-Agent',
                deadline=deadline,
                category='Regular'
            )
            
            if task_id:
                saved_count += 1
                print(f"✅ Saved: {task['title'][:50]}... (Task #{task_id})")
            else:
                failed_count += 1
                print(f"❌ Failed: {task['title'][:50]}...")
                
        except Exception as e:
            failed_count += 1
            print(f"❌ Error saving '{task['title'][:30]}...': {e}")
    
    print(f"\n📊 Results: {saved_count} saved, {failed_count} failed")
    
    if saved_count > 0:
        print("\n🎉 THE EXTRACTOR CAN SAVE TASKS!")
    else:
        print("\n❌ NO TASKS WERE SAVED - there's a bug in the save logic")
        
except Exception as e:
    print(f"❌ Simulation failed: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)
