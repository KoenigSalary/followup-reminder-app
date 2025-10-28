"""
Email Preferences Management for Followup Reminder System
Handles user email notification preferences
"""

import json
from pathlib import Path
from datetime import datetime

DATA_DIR = Path("data")
PREFERENCES_FILE = DATA_DIR / "email_preferences.json"

class EmailPreferences:
    def __init__(self):
        self.preferences_file = PREFERENCES_FILE
        self._ensure_data_dir()
    
    def _ensure_data_dir(self):
        """Ensure data directory exists"""
        DATA_DIR.mkdir(exist_ok=True)
    
    def load_preferences(self):
        """Load all user preferences"""
        if self.preferences_file.exists():
            with open(self.preferences_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_preferences(self, preferences):
        """Save all user preferences"""
        with open(self.preferences_file, 'w') as f:
            json.dump(preferences, f, indent=2)
    
    def get_user_preferences(self, username):
        """Get preferences for a specific user"""
        all_prefs = self.load_preferences()
        
        # Default preferences
        default_prefs = {
            'email_enabled': True,
            'alternate_digest': True,
            'deadline_alerts': True,
            'weekly_summary': True,
            'status_changes': True,
            'completion_celebration': True,
            'created_at': datetime.now().isoformat()
        }
        
        return all_prefs.get(username, default_prefs)
    
    def update_user_preferences(self, username, preferences):
        """Update preferences for a specific user"""
        all_prefs = self.load_preferences()
        all_prefs[username] = preferences
        all_prefs[username]['updated_at'] = datetime.now().isoformat()
        self.save_preferences(all_prefs)
        return True
    
    def should_send_email(self, username, email_type):
        """Check if user should receive specific email type"""
        prefs = self.get_user_preferences(username)
        
        # Check if emails are enabled at all
        if not prefs.get('email_enabled', True):
            return False
        
        # Check specific email type
        return prefs.get(email_type, True)
    
    def get_item_recipients(self, item):
        """
        Get list of email recipients for an item based on item settings
        Returns: {
            'to': [primary_email],
            'cc': [cc_emails],
            'additional': [other_emails]
        }
        """
        recipients = {
            'to': [],
            'cc': [],
            'additional': []
        }
        
        # Primary recipient: responsible person (if send_to_responsible is enabled)
        if item.get('send_to_responsible', True) and item.get('responsible_email'):
            recipients['to'].append(item['responsible_email'])
        
        # CC owner if enabled
        if item.get('cc_owner', True) and item.get('owner_email'):
            recipients['cc'].append(item['owner_email'])
        
        # Additional recipients
        if item.get('additional_recipients'):
            recipients['additional'] = item['additional_recipients']
        
        # Fallback: if no recipients specified, send to owner
        if not recipients['to'] and not recipients['cc'] and not recipients['additional']:
            if item.get('owner_email'):
                recipients['to'].append(item['owner_email'])
        
        return recipients
    
    def get_all_recipients(self, item):
        """Get flat list of all unique email recipients for an item"""
        recipients = self.get_item_recipients(item)
        all_emails = recipients['to'] + recipients['cc'] + recipients['additional']
        # Remove duplicates and None values
        return list(set([email for email in all_emails if email]))
