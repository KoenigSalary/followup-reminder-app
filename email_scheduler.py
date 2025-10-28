"""
Email Scheduler for Followup Reminder System
Handles scheduled email sending:
- Alternate day digest (every 2 days at 8 AM)
- Weekly summary (every Monday at 8 AM)
- Real-time deadline alerts (checks throughout the day)
"""

import schedule
import time
import json
from datetime import datetime, timedelta
from pathlib import Path
from email_service import EmailService
import threading

class EmailScheduler:
    def __init__(self):
        self.email_service = EmailService()
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
    
    def send_alternate_day_digest_job(self):
        """Job to send alternate day digest"""
        print(f"[{datetime.now()}] Checking alternate day digest...")
        
        if not self.should_send_alternate_digest():
            print("Not time for alternate digest yet")
            return
        
        items = self.load_items()
        users = self.load_users()
        
        # Group items by user
        for username, user_data in users.items():
            user_email = user_data.get('email')
            if not user_email:
                continue
            
            user_items = [item for item in items if item.get('owner') == username]
            
            # Generate digest
            email_data = self.email_service.generate_alternate_day_digest(user_items, user_email)
            
            if email_data:
                success = self.email_service.send_email(
                    user_email,
                    email_data['subject'],
                    email_data['html_content'],
                    email_data['plain_content']
                )
                
                if success:
                    print(f"✅ Alternate digest sent to {user_email}")
        
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
        
        for username, user_data in users.items():
            user_email = user_data.get('email')
            if not user_email:
                continue
            
            user_items = [item for item in items if item.get('owner') == username]
            
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
            email_data = self.email_service.generate_weekly_summary(user_items, user_email, stats)
            
            if email_data:
                success = self.email_service.send_email(
                    user_email,
                    email_data['subject'],
                    email_data['html_content'],
                    email_data['plain_content']
                )
                
                if success:
                    print(f"✅ Weekly summary sent to {user_email}")
        
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
                    # Get user email
                    username = item.get('owner')
                    if username and username in users:
                        user_email = users[username].get('email')
                        
                        if user_email:
                            email_data = self.email_service.generate_deadline_alert(item, user_email)
                            
                            if email_data:
                                success = self.email_service.send_email(
                                    user_email,
                                    email_data['subject'],
                                    email_data['html_content'],
                                    email_data['plain_content']
                                )
                                
                                if success:
                                    print(f"✅ Deadline alert sent for item #{item['id']}")
                                    # Mark as alerted
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
        print("📅 Email scheduler running in background")

# Standalone script to run scheduler
if __name__ == "__main__":
    scheduler = EmailScheduler()
    scheduler.run()
