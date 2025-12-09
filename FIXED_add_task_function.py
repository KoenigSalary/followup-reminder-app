"""
Fixed add_task function for mom_agent.py
Replace the existing add_task function with this one
"""

import pandas as pd
from datetime import datetime
import yaml

# Load config
with open('config.yaml', 'r', encoding='utf-8') as f:
    config = yaml.safe_load(f)

MOM_FILE = config['paths']['mom_file']

def add_task(meeting_id, title, details, department, assigned_to, created_by, deadline, category='Regular'):
    """
    Add a new task to MoM_Master.xlsx
    
    FIXED VERSION - Actually saves tasks to Excel
    """
    try:
        # Read existing tasks
        df = pd.read_excel(MOM_FILE, sheet_name='Tasks')
        
        # Get next TaskID
        if len(df) > 0 and 'TaskID' in df.columns:
            next_id = df['TaskID'].max() + 1
        else:
            next_id = 1
        
        # Create new task row
        new_task = {
            'TaskID': next_id,
            'MeetingID': meeting_id,
            'Title': title,
            'Details': details,
            'Department': department,
            'AssignedTo': assigned_to,
            'CreatedBy': created_by,
            'CreatedDate': datetime.now(),
            'Deadline': deadline,
            'Status': 'pending',
            'LastUpdateDate': datetime.now(),
            'LastUpdateBy': created_by
        }
        
        # Add Category column if it exists
        if 'Category' in df.columns:
            new_task['Category'] = category
        
        # Append new task
        df = pd.concat([df, pd.DataFrame([new_task])], ignore_index=True)
        
        # Write back to Excel
        with pd.ExcelWriter(MOM_FILE, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, sheet_name='Tasks', index=False)
        
        print(f"✅ Saved task #{next_id}: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Error saving task: {e}")
        import traceback
        traceback.print_exc()
        return False
