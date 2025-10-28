# 📧 Email Notification Setup Guide

## Complete Email System Features

Your app now includes a **Full Email Notification System** with:

### ✅ What You'll Receive:

1. **Alternate Day Digest** (Every 2 days at 8 AM)
   - High and Urgent priority items only
   - Titles + Deadlines + MOM points
   - Color-coded by urgency

2. **Real-time Deadline Alerts** (4 days before deadline)
   - Individual emails per item
   - Triggered automatically
   - Action buttons included

3. **Weekly Summary** (Every Monday at 8 AM)
   - All pending items
   - Completion statistics
   - Performance metrics

4. **Status Change Notifications**
   - When item status changes
   - Instant notifications

5. **Completion Celebrations** 🎉
   - When you complete a task
   - Motivational messages

6. **Email Reply Functionality**
   - Update status by replying to emails
   - Simple commands like "Item #5 completed"

---

## 🚀 Quick Setup (15 minutes)

### Step 1: Generate Gmail App Password

**Why App Password?**
- Gmail doesn't allow regular passwords for apps
- More secure
- Can be revoked without changing Gmail password

**How to Generate:**

1. **Go to Google Account**
   - Visit: https://myaccount.google.com/
   - Sign in with your Gmail account

2. **Enable 2-Factor Authentication** (if not already)
   - Go to: https://myaccount.google.com/security
   - Find "2-Step Verification"
   - Click "Get Started" and follow instructions
   - **This is required** for App Passwords

3. **Create App Password**
   - Go to: https://myaccount.google.com/apppasswords
   - Or search "App Passwords" in Google Account settings
   - Select app: "Mail"
   - Select device: "Other (Custom name)"
   - Name it: "Followup Reminder App"
   - Click "Generate"

4. **Copy the 16-Character Password**
   - Looks like: `abcd efgh ijkl mnop`
   - **Save this** - you won't see it again!
   - Remove spaces when using: `abcdefghijklmnop`

---

### Step 2: Configure Streamlit Cloud Secrets

**Add Email Credentials to Your Deployed App:**

1. **Go to Streamlit Cloud Dashboard**
   - Visit: https://share.streamlit.io
   - Find your app: `followup-reminder-app`
   - Click the ⋮ menu (three dots)
   - Select "Settings"

2. **Add Secrets**
   - Click "Secrets" tab
   - Add this configuration:

```toml
# Email Configuration
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password-here"
APP_URL = "https://your-app-url.streamlit.app"

# Email Settings
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

**Replace:**
- `your-email@gmail.com` - Your Gmail address
- `your-app-password-here` - The 16-character app password (no spaces)
- `https://your-app-url.streamlit.app` - Your actual Streamlit app URL

3. **Save Secrets**
   - Click "Save"
   - App will automatically restart

---

### Step 3: Test Email Functionality

**Testing Locally (Optional):**

Before deploying, test on your Mac:

```bash
cd ~/Downloads/followup_reminder_app

# Set environment variables
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export APP_URL="http://localhost:8501"

# Run app
streamlit run app.py
```

**Add a test item with deadline in 4 days** to test deadline alerts!

---

### Step 4: Deploy Updated Code

```bash
cd ~/Downloads/followup_reminder_app

# Add new files
git add email_service.py
git add email_scheduler.py
git add requirements.txt
git add EMAIL_SETUP_GUIDE.md

# Commit
git commit -m "Add full email notification system"

# Push
git push
```

**Streamlit Cloud will auto-update in 1-2 minutes!**

---

## 📧 Email Schedules

### Alternate Day Digest
- **When:** Every 2 days at 8:00 AM
- **Content:** High/Urgent priority items only
- **Includes:** Title, Deadline, MOM point, Days left
- **Purpose:** Keep focus on critical items

### Weekly Summary
- **When:** Every Monday at 8:00 AM
- **Content:** All pending items + statistics
- **Includes:** Completion rate, pending count, charts
- **Purpose:** Weekly performance review

### Deadline Alerts
- **When:** Exactly 4 days before deadline
- **Content:** Individual item details
- **Includes:** Direct action buttons, reply options
- **Purpose:** Proactive deadline management

### Status Change Notifications
- **When:** Immediately when status changes
- **Content:** Old status → New status
- **Purpose:** Keep track of progress

### Completion Celebrations
- **When:** Item marked as Completed
- **Content:** Congratulations message
- **Purpose:** Motivation and positive reinforcement

---

## 🔄 Email Reply Functionality

### How to Update Status via Email

**Simple Commands:**

Reply to any email with these commands:

```
Item #5 completed
Item #3 in progress
Item #7 pending
Item #2 blocked
```

**Alternative Phrases:**

```
# For Completed:
- Item #5 done
- Item #5 finished

# For In Progress:
- Item #3 working
- Item #3 started

# For Blocked:
- Item #2 stuck
- Item #2 waiting
```

**The system automatically:**
1. Parses your reply
2. Finds the item ID
3. Updates the status
4. Sends confirmation email

---

## 🎨 Email Templates

### Alternate Day Digest Email
```
Subject: 🔴 Priority Items Digest - October 28, 2025

[Koenig Logo]

Hi there! 👋

Here are your High and Urgent priority followup items:

🚨 URGENT Items (2)
━━━━━━━━━━━━━━━━━━━━━━
#5: Finalize Q4 Budget Report
📅 Deadline: Nov 1, 2025 (4 days left)
👤 Praveen | 📁 Team Meeting | 📌 Pending
📝 Boss requested complete budget analysis with projections...

🔴 HIGH Priority Items (3)
━━━━━━━━━━━━━━━━━━━━━━
...

[Open App Button]

💡 Tip: Reply with "Item #5 completed" to update status!
```

### Deadline Alert Email
```
Subject: ⏰ Deadline Alert: Q4 Budget Report - Due in 4 Days

⏰ DEADLINE ALERT
Action Required - Due in 4 Days

🔔 Finalize Q4 Budget Report

⏱️ Due in 4 days - November 1, 2025

📋 Category: Team Meeting
⚡ Priority: Urgent
👤 Responsible: Praveen
📌 Status: Pending

📝 MOM Point:
Boss requested complete budget analysis with projections for next quarter...

⚠️ This item is due in 4 days. Please take action soon!

[Update Status Button] [Reply to Update Button]
```

### Weekly Summary Email
```
Subject: 📊 Weekly Summary - 12 Pending Items

📊 WEEKLY SUMMARY
Week of October 28, 2025

Your Weekly Performance
━━━━━━━━━━━━━━━━━━━━━━

┌─────────┬─────────┬─────────┬─────────┐
│  Total  │Complete │ Pending │  Rate   │
│   25    │   13    │   12    │   52%   │
└─────────┴─────────┴─────────┴─────────┘

📋 Pending Items (12)

🚨 URGENT (2)
🔴 HIGH (4)
🟡 MEDIUM (5)
🟢 LOW (1)

[View All Items Button]

💡 This Week's Tips:
- Focus on 2 urgent items first
- Aim for 80%+ completion rate
- Review and update status daily
```

---

## ⚙️ Advanced Configuration

### Customize Email Timing

Edit `email_scheduler.py`:

```python
# Change from 8 AM to 9 AM
schedule.every().day.at("09:00").do(self.send_alternate_day_digest_job)

# Change from every 6 hours to every 12 hours
schedule.every(12).hours.do(self.check_deadline_alerts_job)

# Change from Monday to Friday
schedule.every().friday.at("17:00").do(self.send_weekly_summary_job)
```

### Customize Deadline Alert Days

Edit `email_service.py`:

```python
# Change from 4 days to 7 days before
if days_left == 7:  # Instead of days_left == 4
```

### Use Different Email Provider

**For Outlook/Office 365:**
```toml
SMTP_SERVER = "smtp-mail.outlook.com"
SMTP_PORT = 587
```

**For Yahoo:**
```toml
SMTP_SERVER = "smtp.mail.yahoo.com"
SMTP_PORT = 587
```

**For SendGrid (Professional):**
```toml
SMTP_SERVER = "smtp.sendgrid.net"
SMTP_PORT = 587
SENDER_EMAIL = "apikey"
SENDER_PASSWORD = "your-sendgrid-api-key"
```

---

## 🆘 Troubleshooting

### Emails Not Sending

**Check 1: Verify Secrets**
```
Go to Streamlit Cloud → App Settings → Secrets
Make sure all values are correct (no extra spaces)
```

**Check 2: Gmail App Password**
```
- Is 2FA enabled on your Gmail?
- Did you remove spaces from app password?
- Try generating a new app password
```

**Check 3: Check App Logs**
```
Streamlit Cloud → Your App → Logs
Look for email-related errors
```

### Emails Going to Spam

**Fix:**
- Check your Gmail spam folder
- Mark email as "Not Spam"
- Add sender email to contacts
- Gmail will learn over time

### Not Receiving Deadline Alerts

**Check:**
- Is deadline exactly 4 days away?
- Is item status NOT "Completed"?
- Check `data/last_digest.json` for tracking
- Has the alert already been sent for this item?

### Email Reply Not Working

**Verify:**
- Reply format: "Item #5 completed" (exact format)
- Reply to the original email (not forward)
- Check app logs for parsing errors

---

## 📊 Email Analytics

### Track Email Performance

Check `data/last_digest.json`:
```json
{
  "last_alternate_digest": "2025-10-28T08:00:00",
  "last_weekly_summary": "2025-10-28T08:00:00",
  "deadline_alerts_sent": [5, 12, 18, 23]
}
```

- `last_alternate_digest`: When last digest was sent
- `last_weekly_summary`: When last weekly summary was sent
- `deadline_alerts_sent`: Item IDs that have been alerted

---

## 🔒 Security Best Practices

1. **Never share your App Password**
   - Keep it secret
   - Store only in Streamlit secrets
   - Don't commit to GitHub

2. **Use App Passwords, not regular passwords**
   - More secure
   - Can be revoked independently
   - Specific to this app

3. **Enable 2FA on Gmail**
   - Required for App Passwords
   - Extra security layer

4. **Regularly rotate passwords**
   - Change app password every 3-6 months
   - Update in Streamlit secrets

5. **Monitor email logs**
   - Check for suspicious activity
   - Review sent emails regularly

---

## 🎯 Testing Checklist

After setup, verify:

- [ ] Secrets configured in Streamlit Cloud
- [ ] App restarted successfully
- [ ] Add item with deadline in 4 days
- [ ] Check for deadline alert email (wait for scheduled check)
- [ ] Add High/Urgent priority items
- [ ] Wait for alternate digest (or trigger manually)
- [ ] Complete an item - check for celebration email
- [ ] Change status - check for notification email
- [ ] Reply to email with status update
- [ ] Check logs for any errors

---

## 💡 Pro Tips

1. **Test with Your Own Email First**
   - Make sure everything works
   - Before sharing with team

2. **Whitelist Sender Email**
   - Add to contacts
   - Prevents spam folder issues

3. **Check Emails Morning & Evening**
   - 8 AM: Digest/Summary
   - Throughout day: Deadline alerts

4. **Use Email Reply Feature**
   - Quick status updates
   - No need to open app

5. **Monitor Weekly Summaries**
   - Track your completion rate
   - Aim for 80%+ performance

---

## 🚀 Next Steps

1. ✅ **Setup Gmail App Password** (5 min)
2. ✅ **Configure Streamlit Secrets** (3 min)
3. ✅ **Push updated code** (2 min)
4. ✅ **Test with sample items** (5 min)
5. ✅ **Share with team** once working!

---

**Your comprehensive email notification system is ready! 🎉📧**

Questions? Check the troubleshooting section or review app logs!
