"""
Email Service for Followup Reminder System
Handles all email notifications including:
- Alternate day digest (High/Urgent priority)
- Real-time deadline alerts (4 days before)
- Weekly summary (all pending items)
- Status change notifications
- Email reply functionality
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
import json
from pathlib import Path
import hashlib

class EmailService:
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.app_url = os.getenv("APP_URL", "https://your-app.streamlit.app")
        
    def send_email(self, recipient_email, subject, html_content, plain_content=None):
        """Send email with HTML and plain text fallback"""
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.sender_email
            msg['To'] = recipient_email
            msg['Reply-To'] = self.sender_email
            
            # Add plain text version
            if plain_content:
                part1 = MIMEText(plain_content, 'plain')
                msg.attach(part1)
            
            # Add HTML version
            part2 = MIMEText(html_content, 'html')
            msg.attach(part2)
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    def generate_alternate_day_digest(self, items, user_email):
        """Generate alternate day digest email (High/Urgent priority only)"""
        # Filter High/Urgent priority items
        high_urgent_items = [
            item for item in items 
            if item['priority'] in ['High', 'Urgent'] and item['status'] != 'Completed'
        ]
        
        if not high_urgent_items:
            return None
        
        subject = f"🔴 Priority Items Digest - {datetime.now().strftime('%B %d, %Y')}"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                          color: white; padding: 20px; text-align: center; }}
                .container {{ padding: 20px; max-width: 600px; margin: 0 auto; }}
                .item {{ background: #f9f9f9; border-left: 4px solid #ff4b4b; 
                        padding: 15px; margin: 15px 0; border-radius: 5px; }}
                .item.urgent {{ border-left-color: #ff0000; background: #fff5f5; }}
                .item.high {{ border-left-color: #ff4b4b; }}
                .deadline {{ color: #666; font-size: 14px; }}
                .priority {{ display: inline-block; padding: 4px 8px; border-radius: 3px; 
                           font-size: 12px; font-weight: bold; }}
                .priority.urgent {{ background: #ff0000; color: white; }}
                .priority.high {{ background: #ff4b4b; color: white; }}
                .mom-point {{ background: #e8f4f8; padding: 10px; margin-top: 10px; 
                            border-radius: 5px; font-style: italic; }}
                .footer {{ text-align: center; margin-top: 30px; padding: 20px; 
                          background: #f0f0f0; font-size: 12px; }}
                .btn {{ display: inline-block; padding: 10px 20px; background: #667eea; 
                       color: white; text-decoration: none; border-radius: 5px; margin: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>🔴 Priority Items Digest</h1>
                <p>{datetime.now().strftime('%A, %B %d, %Y')}</p>
            </div>
            <div class="container">
                <p>Hi there! 👋</p>
                <p>Here are your <strong>High and Urgent priority</strong> followup items:</p>
                <h3>Total Priority Items: {len(high_urgent_items)}</h3>
        """
        
        # Group by priority
        urgent_items = [i for i in high_urgent_items if i['priority'] == 'Urgent']
        high_items = [i for i in high_urgent_items if i['priority'] == 'High']
        
        if urgent_items:
            html_content += "<h3>🚨 URGENT Items</h3>"
            for item in urgent_items:
                days_left = self._get_days_left(item.get('deadline'))
                html_content += self._format_item_html(item, days_left, 'urgent')
        
        if high_items:
            html_content += "<h3>🔴 HIGH Priority Items</h3>"
            for item in high_items:
                days_left = self._get_days_left(item.get('deadline'))
                html_content += self._format_item_html(item, days_left, 'high')
        
        html_content += f"""
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{self.app_url}" class="btn">📋 Open App</a>
                </div>
            </div>
            <div class="footer">
                <p>💡 <strong>Tip:</strong> Reply to this email with item ID and status to update!</p>
                <p>Example: "Item #5 completed" or "Item #3 in progress"</p>
                <p>This is an automated message from Followup Reminder System</p>
            </div>
        </body>
        </html>
        """
        
        plain_content = self._generate_plain_text_digest(high_urgent_items)
        
        return {
            'subject': subject,
            'html_content': html_content,
            'plain_content': plain_content
        }
    
    def generate_deadline_alert(self, item, user_email):
        """Generate real-time deadline alert (4 days before deadline)"""
        days_left = self._get_days_left(item.get('deadline'))
        
        if days_left != 4:  # Only send 4 days before
            return None
        
        subject = f"⏰ Deadline Alert: {item['title']} - Due in 4 Days"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: #ff9800; color: white; padding: 20px; text-align: center; }}
                .container {{ padding: 20px; max-width: 600px; margin: 0 auto; }}
                .alert-box {{ background: #fff3cd; border: 2px solid #ff9800; 
                            padding: 20px; border-radius: 10px; margin: 20px 0; }}
                .item-details {{ background: #f9f9f9; padding: 15px; border-radius: 5px; 
                               margin: 15px 0; }}
                .btn {{ display: inline-block; padding: 12px 24px; background: #667eea; 
                       color: white; text-decoration: none; border-radius: 5px; margin: 10px 5px; }}
                .btn-secondary {{ background: #6c757d; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>⏰ Deadline Alert</h1>
                <p>Action Required - Due in 4 Days</p>
            </div>
            <div class="container">
                <div class="alert-box">
                    <h2>🔔 {item['title']}</h2>
                    <p><strong>⏱️ Due in 4 days</strong> - {item.get('deadline', 'Not set')}</p>
                </div>
                
                <div class="item-details">
                    <p><strong>📋 Category:</strong> {item['category']}</p>
                    <p><strong>⚡ Priority:</strong> {item['priority']}</p>
                    <p><strong>👤 Responsible:</strong> {item['responsible']}</p>
                    <p><strong>📌 Status:</strong> {item['status']}</p>
                    
                    {f'<div class="mom-point"><strong>📝 MOM Point:</strong><br>{item["description"]}</div>' 
                     if item.get('description') else ''}
                </div>
                
                <p>⚠️ This item is due in <strong>4 days</strong>. Please take action soon!</p>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{self.app_url}" class="btn">📋 Update Status</a>
                    <a href="mailto:{self.sender_email}?subject=Item #{item['id']} Update&body=Item #{item['id']} status: " 
                       class="btn btn-secondary">📧 Reply to Update</a>
                </div>
            </div>
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f0f0f0; font-size: 12px;">
                <p>💡 Reply with: "Item #{item['id']} completed" to mark as done</p>
                <p>Or: "Item #{item['id']} in progress" to update status</p>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
DEADLINE ALERT - Due in 4 Days
==============================

Title: {item['title']}
Deadline: {item.get('deadline', 'Not set')}
Priority: {item['priority']}
Category: {item['category']}
Responsible: {item['responsible']}
Status: {item['status']}

MOM Point:
{item.get('description', 'N/A')}

Action Required: This item is due in 4 days!

Open App: {self.app_url}

To update via email, reply with:
"Item #{item['id']} completed" or "Item #{item['id']} in progress"
        """
        
        return {
            'subject': subject,
            'html_content': html_content,
            'plain_content': plain_content
        }
    
    def generate_weekly_summary(self, items, user_email, stats):
        """Generate weekly summary email (all pending items)"""
        pending_items = [i for i in items if i['status'] != 'Completed']
        
        subject = f"📊 Weekly Summary - {len(pending_items)} Pending Items"
        
        html_content = f"""
        <html>
        <head>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .header {{ background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                          color: white; padding: 20px; text-align: center; }}
                .container {{ padding: 20px; max-width: 600px; margin: 0 auto; }}
                .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
                .stat-box {{ background: #f0f0f0; padding: 15px; border-radius: 10px; 
                           text-align: center; flex: 1; margin: 5px; }}
                .stat-number {{ font-size: 32px; font-weight: bold; color: #667eea; }}
                .item-list {{ margin: 20px 0; }}
                .item {{ background: #f9f9f9; padding: 12px; margin: 10px 0; 
                        border-left: 4px solid #667eea; border-radius: 5px; }}
                .btn {{ display: inline-block; padding: 12px 24px; background: #667eea; 
                       color: white; text-decoration: none; border-radius: 5px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>📊 Weekly Summary</h1>
                <p>Week of {datetime.now().strftime('%B %d, %Y')}</p>
            </div>
            <div class="container">
                <h2>Your Weekly Performance</h2>
                
                <div class="stats">
                    <div class="stat-box">
                        <div class="stat-number">{stats.get('total', 0)}</div>
                        <div>Total Items</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{stats.get('completed', 0)}</div>
                        <div>Completed</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{stats.get('pending', 0)}</div>
                        <div>Pending</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-number">{stats.get('completion_rate', 0)}%</div>
                        <div>Completion Rate</div>
                    </div>
                </div>
                
                <h3>📋 Pending Items ({len(pending_items)})</h3>
                <div class="item-list">
        """
        
        # Group pending items by priority
        urgent = [i for i in pending_items if i['priority'] == 'Urgent']
        high = [i for i in pending_items if i['priority'] == 'High']
        medium = [i for i in pending_items if i['priority'] == 'Medium']
        low = [i for i in pending_items if i['priority'] == 'Low']
        
        for priority_name, priority_items in [('🚨 URGENT', urgent), ('🔴 HIGH', high), 
                                               ('🟡 MEDIUM', medium), ('🟢 LOW', low)]:
            if priority_items:
                html_content += f"<h4>{priority_name} ({len(priority_items)})</h4>"
                for item in priority_items[:5]:  # Show top 5 per priority
                    days_left = self._get_days_left(item.get('deadline'))
                    html_content += f"""
                    <div class="item">
                        <strong>#{item['id']}: {item['title']}</strong><br>
                        📅 Deadline: {item.get('deadline', 'Not set')} 
                        {f'({days_left} days left)' if days_left is not None else ''}<br>
                        👤 {item['responsible']} | 📁 {item['category']}
                    </div>
                    """
        
        html_content += f"""
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{self.app_url}" class="btn">📋 View All Items</a>
                </div>
                
                <div style="margin-top: 30px; padding: 15px; background: #e8f4f8; border-radius: 5px;">
                    <h4>💡 This Week's Tips:</h4>
                    <ul>
                        <li>Focus on {len(urgent)} urgent items first</li>
                        <li>Aim for 80%+ completion rate</li>
                        <li>Review and update status daily</li>
                    </ul>
                </div>
            </div>
            <div style="text-align: center; margin-top: 30px; padding: 20px; background: #f0f0f0; font-size: 12px;">
                <p>Weekly summaries are sent every Monday at 8 AM</p>
                <p>Reply to this email to update item status</p>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
WEEKLY SUMMARY - {datetime.now().strftime('%B %d, %Y')}
========================================

Statistics:
- Total Items: {stats.get('total', 0)}
- Completed: {stats.get('completed', 0)}
- Pending: {stats.get('pending', 0)}
- Completion Rate: {stats.get('completion_rate', 0)}%

Pending Items: {len(pending_items)}

URGENT: {len(urgent)}
HIGH: {len(high)}
MEDIUM: {len(medium)}
LOW: {len(low)}

View all items: {self.app_url}
        """
        
        return {
            'subject': subject,
            'html_content': html_content,
            'plain_content': plain_content
        }
    
    def send_status_change_notification(self, item, old_status, new_status, user_email):
        """Send notification when item status changes"""
        subject = f"✅ Status Updated: {item['title']}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="background: #667eea; color: white; padding: 20px; text-align: center;">
                <h2>Status Updated</h2>
            </div>
            <div style="padding: 20px; max-width: 600px; margin: 0 auto;">
                <h3>{item['title']}</h3>
                <p><strong>Status changed from:</strong> {old_status} → {new_status}</p>
                
                <div style="background: #f9f9f9; padding: 15px; border-radius: 5px; margin: 15px 0;">
                    <p><strong>Priority:</strong> {item['priority']}</p>
                    <p><strong>Deadline:</strong> {item.get('deadline', 'Not set')}</p>
                    <p><strong>Category:</strong> {item['category']}</p>
                </div>
                
                {f'<p><strong>Description:</strong><br>{item.get("description", "")}</p>' 
                 if item.get('description') else ''}
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{self.app_url}" 
                       style="display: inline-block; padding: 12px 24px; background: #667eea; 
                              color: white; text-decoration: none; border-radius: 5px;">
                        View in App
                    </a>
                </div>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
STATUS UPDATED
==============

{item['title']}

Status: {old_status} → {new_status}

Priority: {item['priority']}
Deadline: {item.get('deadline', 'Not set')}
Category: {item['category']}

View in app: {self.app_url}
        """
        
        return {
            'subject': subject,
            'html_content': html_content,
            'plain_content': plain_content
        }
    
    def send_completion_notification(self, item, user_email):
        """Send notification when item is completed"""
        subject = f"🎉 Completed: {item['title']}"
        
        html_content = f"""
        <html>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%); 
                        color: white; padding: 30px; text-align: center;">
                <h1>🎉 Congratulations!</h1>
                <h2>Task Completed</h2>
            </div>
            <div style="padding: 20px; max-width: 600px; margin: 0 auto;">
                <h3>✅ {item['title']}</h3>
                
                <div style="background: #d4edda; border: 2px solid #28a745; padding: 20px; 
                           border-radius: 10px; margin: 20px 0; text-align: center;">
                    <p style="font-size: 18px; margin: 0;">
                        <strong>Great job completing this task! 🎊</strong>
                    </p>
                </div>
                
                <div style="background: #f9f9f9; padding: 15px; border-radius: 5px;">
                    <p><strong>Category:</strong> {item['category']}</p>
                    <p><strong>Priority:</strong> {item['priority']}</p>
                    <p><strong>Completed on:</strong> {datetime.now().strftime('%B %d, %Y')}</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{self.app_url}" 
                       style="display: inline-block; padding: 12px 24px; background: #28a745; 
                              color: white; text-decoration: none; border-radius: 5px;">
                        View Dashboard
                    </a>
                </div>
                
                <p style="text-align: center; margin-top: 30px; color: #666; font-style: italic;">
                    Keep up the great work! 💪
                </p>
            </div>
        </body>
        </html>
        """
        
        plain_content = f"""
🎉 TASK COMPLETED!
==================

{item['title']}

Great job completing this task!

Category: {item['category']}
Priority: {item['priority']}
Completed: {datetime.now().strftime('%B %d, %Y')}

View dashboard: {self.app_url}

Keep up the great work! 💪
        """
        
        return {
            'subject': subject,
            'html_content': html_content,
            'plain_content': plain_content
        }
    
    def _format_item_html(self, item, days_left, priority_class):
        """Format individual item for HTML email"""
        return f"""
        <div class="item {priority_class}">
            <div>
                <strong>#{item['id']}: {item['title']}</strong>
                <span class="priority {priority_class}">{item['priority']}</span>
            </div>
            <div class="deadline">
                📅 Deadline: {item.get('deadline', 'Not set')} 
                {f'({days_left} days left)' if days_left is not None else ''}
            </div>
            <div class="deadline">
                👤 {item['responsible']} | 📁 {item['category']} | 📌 {item['status']}
            </div>
            {f'<div class="mom-point">📝 {item.get("description", "")[:200]}...</div>' 
             if item.get('description') else ''}
        </div>
        """
    
    def _generate_plain_text_digest(self, items):
        """Generate plain text version of digest"""
        text = f"PRIORITY ITEMS DIGEST - {datetime.now().strftime('%B %d, %Y')}\n"
        text += "=" * 50 + "\n\n"
        text += f"Total Priority Items: {len(items)}\n\n"
        
        for item in items:
            days_left = self._get_days_left(item.get('deadline'))
            text += f"#{item['id']}: {item['title']}\n"
            text += f"  Priority: {item['priority']}\n"
            text += f"  Deadline: {item.get('deadline', 'Not set')}"
            if days_left is not None:
                text += f" ({days_left} days left)"
            text += f"\n  Responsible: {item['responsible']}\n"
            text += f"  Category: {item['category']}\n"
            if item.get('description'):
                text += f"  MOM: {item['description'][:100]}...\n"
            text += "\n"
        
        text += f"\nOpen app: {self.app_url}\n"
        return text
    
    def _get_days_left(self, deadline_str):
        """Calculate days left until deadline"""
        if not deadline_str:
            return None
        try:
            deadline = datetime.fromisoformat(deadline_str).date()
            today = datetime.now().date()
            return (deadline - today).days
        except:
            return None
    
    def parse_email_reply(self, email_body):
        """Parse email reply to extract item ID and status update"""
        # Expected format: "Item #5 completed" or "Item #3 in progress"
        import re
        
        patterns = [
            r'item\s*#?(\d+)\s+(completed|done|finished)',
            r'item\s*#?(\d+)\s+(in progress|working|started)',
            r'item\s*#?(\d+)\s+(pending|todo|not started)',
            r'item\s*#?(\d+)\s+(blocked|stuck|waiting)'
        ]
        
        email_body_lower = email_body.lower()
        
        for pattern in patterns:
            match = re.search(pattern, email_body_lower)
            if match:
                item_id = int(match.group(1))
                status_text = match.group(2)
                
                # Map to actual status values
                status_map = {
                    'completed': 'Completed',
                    'done': 'Completed',
                    'finished': 'Completed',
                    'in progress': 'In Progress',
                    'working': 'In Progress',
                    'started': 'In Progress',
                    'pending': 'Pending',
                    'todo': 'Pending',
                    'not started': 'Pending',
                    'blocked': 'Blocked',
                    'stuck': 'Blocked',
                    'waiting': 'Blocked'
                }
                
                new_status = status_map.get(status_text, None)
                if new_status:
                    return {'item_id': item_id, 'new_status': new_status}
        
        return None
