"""
Email Scheduler for Followup Reminder System (Enhanced)
Handles scheduled email sending with flexible recipient control:
- Alternate day digest (every 2 days at 8 AM)
- Weekly summary (every Monday at 8 AM)
- Real-time deadline alerts (checks throughout the day)
- Respects per-item recipient settings (send to responsible, CC owner, additional recipients)
"""

import schedule
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from email_service import EmailService
from email_preferences import EmailPreferences
import threading

class EmailScheduler:
    def __init__(self):
        self.email_service = EmailService()
        self.email_preferences = EmailPreferences()
        self.data_dir = Path("data")
        self.items_file = self.data_dir / "followup_items.json"
        self.users_file = self.data_dir / "users.json"
        self.last_digest_file = self.data_dir / "last_digest.json"
        
        # Track last sent dates
        self.load_tracking_data()
    
    def load_tracking_data(self):
        """Load tracking data for when emails were last sent"""
        if self.last_digest_file.exists():
            with open(self.last_digest_file, 'r') as f:
                self.tracking = json.load(f)
        else:
            self.tracking = {
                'last_alternate_digest': None,
                'last_weekly_summary': None,
                'deadline_alerts_sent': []  # List of item IDs that have been alerted
            }
    
    def save_tracking_data(self):
        """Save tracking data"""
        with open(self.last_digest_file, 'w') as f:
            json.dump(self.tracking, f, indent=2)
    
    def load_items(self):
        """Load followup items"""
        if self.items_file.exists():
            with open(self.items_file, 'r') as f:
                return json.load(f)
        return []
    
    def load_users(self):
        """Load users"""
        if self.users_file.exists():
            with open(self.users_file, 'r') as f:
                return json.load(f)
        return {}
    
    def should_send_alternate_digest(self):
        """Check if 2 days have passed since last digest"""
        if not self.tracking['last_alternate_digest']:
            return True
        
        last_date = datetime.fromisoformat(self.tracking['last_alternate_digest'])
        days_diff = (datetime.now() - last_date).days
        
        return days_diff >= 2
    
    def should_send_weekly_summary(self):
        """Check if it's Monday and weekly summary hasn't been sent this week"""
        if datetime.now().weekday() != 0:  # Not Monday
            return False
        
        if not self.tracking['last_weekly_summary']:
            return True
        
        last_date = datetime.fromisoformat(self.tracking['last_weekly_summary'])
        days_diff = (datetime.now() - last_date).days
        
        return days_diff >= 7
    
    def get_item_recipients(self, item, users):
        """
        Get list of recipients for an item based on item settings
        Returns dict with 'to', 'cc', and 'all_recipients' lists
        """
        recipients = {
            'to': [],
            'cc': [],
            'all_recipients': []
        }
        
        # Check user preferences first
        owner = item.get('owner')
        responsible = item.get('responsible')
        
        # Primary recipient: responsible person (if enabled)
        if item.get('send_to_responsible', True) and responsible:
            responsible_email = item.get('responsible_email')
            if responsible_email:
                # Check if responsible person wants to receive this type of email
                if self.email_preferences.should_send_email(responsible, 'email_enabled'):
                    recipients['to'].append(responsible_email)
                    recipients['all_recipients'].append(responsible_email)
        
        # CC owner if enabled
        if item.get('cc_owner', True) and owner:
            owner_email = item.get('owner_email')
            if owner_email:
                # Check if owner wants to receive this type of email
                if self.email_preferences.should_send_email(owner, 'email_enabled'):
                    recipients['cc'].append(owner_email)
                    recipients['all_recipients'].append(owner_email)
        
        # Additional recipients
        additional = item.get('additional_recipients', [])
        if additional:
            for email in additional:
                # Extract username from email if possible
                # For now, just add the email
                if email not in recipients['all_recipients']:
                    recipients['all_recipients'].append(email)
        
        # Fallback: if no recipients, send to owner
        if not recipients['all_recipients'] and owner:
            owner_email = item.get('owner_email')
            if owner_email:
                recipients['to'].append(owner_email)
                recipients['all_recipients'].append(owner_email)
        
        return recipients
    
    def send_alternate_day_digest_job(self):
        """Job to send alternate day digest"""
        print(f"[{datetime.now()}] Checking alternate day digest...")
        
        if not self.should_send_alternate_digest():
            print("Not time for alternate digest yet")
            return
        
        items = self.load_items()
        users = self.load_users()
        
        # Group items by recipient
        recipient_items = {}  # email -> list of items
        
        for item in items:
            if item['status'] == 'Completed':
                continue
            
            # Get recipients for this item
            recipients = self.get_item_recipients(item, users)
            
            # Add item to each recipient's list
            for email in recipients['all_recipients']:
                if email not in recipient_items:
                    recipient_items[email] = []
                recipient_items[email].append(item)
        
        # Send digest to each recipient
        for email, user_items in recipient_items.items():
            # Check if user wants alternate digest
            # Find username from email
            username = None
            for uname, udata in users.items():
                if udata.get('email') == email:
                    username = uname
                    break
            
            if username and not self.email_preferences.should_send_email(username, 'alternate_digest'):
                print(f"⏭️ Skipping alternate digest for {email} (disabled in preferences)")
                continue
            
            # Generate digest
            email_data = self.email_service.generate_alternate_day_digest(user_items, email)
            
            if email_data:
                success = self.email_service.send_email(
                    email,
                    email_data['subject'],
                    email_data['html_content'],
                    email_data['plain_content']
                )
                
                if success:
                    print(f"✅ Alternate digest sent to {email}")
        
        # Update tracking
        self.tracking['last_alternate_digest'] = datetime.now().isoformat()
        self.save_tracking_data()
    
    def send_weekly_summary_job(self):
        """Job to send weekly summary"""
        print(f"[{datetime.now()}] Checking weekly summary...")
        
        if not self.should_send_weekly_summary():
            print("Not time for weekly summary yet")
            return
        
        items = self.load_items()
        users = self.load_users()
        
        # Group items by recipient
        recipient_items = {}
        
        for item in items:
            recipients = self.get_item_recipients(item, users)
            
            for email in recipients['all_recipients']:
                if email not in recipient_items:
                    recipient_items[email] = []
                recipient_items[email].append(item)
        
        # Send summary to each recipient
        for email, user_items in recipient_items.items():
            # Find username
            username = None
            for uname, udata in users.items():
                if udata.get('email') == email:
                    username = uname
                    break
            
            if username and not self.email_preferences.should_send_email(username, 'weekly_summary'):
                print(f"⏭️ Skipping weekly summary for {email} (disabled in preferences)")
                continue
            
            # Calculate stats
            total = len(user_items)
            completed = len([i for i in user_items if i['status'] == 'Completed'])
            pending = len([i for i in user_items if i['status'] != 'Completed'])
            completion_rate = int((completed / total * 100)) if total > 0 else 0
            
            stats = {
                'total': total,
                'completed': completed,
                'pending': pending,
                'completion_rate': completion_rate
            }
            
            # Generate summary
            email_data = self.email_service.generate_weekly_summary(user_items, email, stats)
            
            if email_data:
                success = self.email_service.send_email(
                    email,
                    email_data['subject'],
                    email_data['html_content'],
                    email_data['plain_content']
                )
                
                if success:
                    print(f"✅ Weekly summary sent to {email}")
        
        # Update tracking
        self.tracking['last_weekly_summary'] = datetime.now().isoformat()
        self.save_tracking_data()
    
    def check_deadline_alerts_job(self):
        """Job to check and send deadline alerts (4 days before)"""
        print(f"[{datetime.now()}] Checking deadline alerts...")
        
        items = self.load_items()
        users = self.load_users()
        
        for item in items:
            # Skip if already alerted or completed
            if item['id'] in self.tracking['deadline_alerts_sent']:
                continue
            
            if item['status'] == 'Completed':
                continue
            
            # Check if deadline is in 4 days
            if not item.get('deadline'):
                continue
            
            try:
                deadline = datetime.fromisoformat(item['deadline']).date()
                today = datetime.now().date()
                days_left = (deadline - today).days
                
                if days_left == 4:  # Exactly 4 days before
                    # Get recipients for this item
                    recipients = self.get_item_recipients(item, users)
                    
                    # Send to each recipient
                    for email in recipients['all_recipients']:
                        # Find username
                        username = None
                        for uname, udata in users.items():
                            if udata.get('email') == email:
                                username = uname
                                break
                        
                        if username and not self.email_preferences.should_send_email(username, 'deadline_alerts'):
                            print(f"⏭️ Skipping deadline alert for {email} (disabled in preferences)")
                            continue
                        
                        email_data = self.email_service.generate_deadline_alert(item, email)
                        
                        if email_data:
                            success = self.email_service.send_email(
                                email,
                                email_data['subject'],
                                email_data['html_content'],
                                email_data['plain_content']
                            )
                            
                            if success:
                                print(f"✅ Deadline alert sent to {email} for item #{item['id']}")
                    
                    # Mark as alerted (only once per item)
                    self.tracking['deadline_alerts_sent'].append(item['id'])
                    self.save_tracking_data()
                    
            except Exception as e:
                print(f"Error checking deadline for item #{item['id']}: {e}")
    
    def setup_schedule(self):
        """Setup all scheduled jobs"""
        # Alternate day digest - Every day at 8:00 AM (will check if 2 days passed)
        schedule.every().day.at("08:00").do(self.send_alternate_day_digest_job)
        
        # Weekly summary - Every Monday at 8:00 AM
        schedule.every().monday.at("08:00").do(self.send_weekly_summary_job)
        
        # Deadline alerts - Check every 6 hours
        schedule.every(6).hours.do(self.check_deadline_alerts_job)
        
        # Also check deadline alerts at 8 AM daily
        schedule.every().day.at("08:00").do(self.check_deadline_alerts_job)
        
        print("📅 Email scheduler setup complete!")
        print("  - Alternate day digest: Daily at 8:00 AM (every 2 days)")
        print("  - Weekly summary: Mondays at 8:00 AM")
        print("  - Deadline alerts: Every 6 hours + 8:00 AM daily")
        print("  - Respects per-item recipient settings and user preferences")
    
    def run(self):
        """Run the scheduler"""
        self.setup_schedule()
        
        print(f"\n🚀 Scheduler started at {datetime.now()}")
        print("Press Ctrl+C to stop\n")
        
        # Run immediately on start (for testing)
        print("Running initial check...")
        self.check_deadline_alerts_job()
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def run_in_background(self):
        """Run scheduler in background thread"""
        def background_job():
            self.setup_schedule()
            while True:
                schedule.run_pending()
                time.sleep(60)
        
        thread = threading.Thread(target=background_job, daemon=True)
        thread.start()
        print("📅 Email scheduler running in background (with flexible recipient control)")

# Standalone script to run scheduler
if __name__ == "__main__":
    scheduler = EmailScheduler()
    scheduler.run()
