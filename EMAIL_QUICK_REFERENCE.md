# 📧 Email Notifications - Quick Reference Card

## 📅 Email Schedule

| Email Type | Frequency | Time | Content |
|------------|-----------|------|---------|
| **Alternate Day Digest** | Every 2 days | 8:00 AM | High/Urgent items only |
| **Weekly Summary** | Every Monday | 8:00 AM | All pending + stats |
| **Deadline Alerts** | 4 days before | Throughout day | Individual items |
| **Status Changes** | Real-time | Immediate | Status updates |
| **Completions** | Real-time | Immediate | Celebration 🎉 |

---

## 📧 Email Reply Commands

### Update Status via Email

**Reply to any email with:**

```
Item #5 completed
Item #3 in progress  
Item #7 pending
Item #2 blocked
```

### Supported Variations:

| Status | Commands |
|--------|----------|
| **Completed** | `completed`, `done`, `finished` |
| **In Progress** | `in progress`, `working`, `started` |
| **Pending** | `pending`, `todo`, `not started` |
| **Blocked** | `blocked`, `stuck`, `waiting` |

**Format:** Always include `Item #` followed by the item number

---

## 🎨 What Each Email Contains

### Alternate Day Digest
- ✅ High & Urgent priority items
- ✅ Titles + Deadlines
- ✅ MOM points (description)
- ✅ Days left countdown
- ✅ Responsible person
- ✅ Quick action links

### Deadline Alert (4 days before)
- ✅ Item title
- ✅ Exact deadline date
- ✅ Priority & Category
- ✅ Full MOM description
- ✅ "Update Status" button
- ✅ Reply-to-update option

### Weekly Summary
- ✅ Total items count
- ✅ Completed vs Pending
- ✅ Completion rate %
- ✅ Pending items by priority
- ✅ Weekly tips
- ✅ Performance insights

### Status Change Notification
- ✅ Item title
- ✅ Old status → New status
- ✅ Item details
- ✅ Link to app

### Completion Celebration
- ✅ Congratulations message 🎉
- ✅ Item details
- ✅ Motivational text
- ✅ Link to dashboard

---

## ⚙️ Quick Setup (Streamlit Cloud)

### 1. Gmail App Password
```
1. Go to: https://myaccount.google.com/apppasswords
2. Generate password for "Mail" app
3. Copy 16-character password (remove spaces)
```

### 2. Streamlit Secrets
```toml
SENDER_EMAIL = "your-email@gmail.com"
SENDER_PASSWORD = "your-app-password"
APP_URL = "https://your-app.streamlit.app"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
```

### 3. Deploy
```bash
git add .
git commit -m "Add email system"
git push
```

---

## 🎯 Email Triggers

### What Triggers Each Email?

1. **Alternate Digest**
   - ⏰ Automatically every 2 days at 8 AM
   - 🎯 Only if you have High/Urgent items

2. **Deadline Alert**
   - ⏰ When deadline is exactly 4 days away
   - 🎯 Checked every 6 hours + daily at 8 AM
   - ⚠️ Only sent once per item

3. **Weekly Summary**
   - ⏰ Every Monday at 8 AM
   - 🎯 Sent to all users
   - 📊 Includes weekly stats

4. **Status Change**
   - ⏰ Immediately when status updated
   - 🎯 Any status change triggers email

5. **Completion**
   - ⏰ When item marked "Completed"
   - 🎉 Celebration message

---

## 🔧 Customization Options

### Change Email Times

Edit `email_scheduler.py`:

```python
# Change digest time
schedule.every().day.at("09:00")  # 9 AM instead of 8 AM

# Change weekly summary day
schedule.every().friday.at("17:00")  # Friday 5 PM

# Change alert frequency
schedule.every(12).hours  # Every 12 hours instead of 6
```

### Change Deadline Alert Days

Edit `email_service.py`:

```python
if days_left == 7:  # Alert 7 days before instead of 4
```

### Change Alternate Digest Frequency

Edit `email_scheduler.py`:

```python
return days_diff >= 3  # Every 3 days instead of 2
```

---

## 🆘 Troubleshooting Quick Fixes

| Problem | Quick Fix |
|---------|-----------|
| **No emails arriving** | Check Streamlit secrets, verify app password |
| **Emails in spam** | Mark as "Not Spam", add to contacts |
| **Reply not working** | Use exact format: `Item #5 completed` |
| **Deadline alert not sent** | Check if exactly 4 days away, item not completed |
| **Duplicate emails** | Check `last_digest.json`, restart app |

---

## 📱 Mobile Email Tips

### iPhone/iPad:
- ✅ Emails display perfectly in Mail app
- ✅ "Open App" button works
- ✅ Reply feature works in Mail
- ✅ Add sender to VIP for notifications

### Android:
- ✅ Works in Gmail app
- ✅ HTML formatting supported
- ✅ Quick reply available
- ✅ Set priority for sender

---

## 💡 Pro Tips

1. **Check emails at consistent times**
   - 8 AM: Digest/Summary
   - Throughout day: Alerts

2. **Use reply feature for quick updates**
   - Faster than opening app
   - Works from mobile

3. **Whitelist sender email**
   - Never miss important alerts
   - Prevents spam folder

4. **Monitor completion rate in weekly summary**
   - Track your productivity
   - Aim for 80%+

5. **Set up email filters**
   - Label by priority
   - Auto-categorize

---

## 📊 Example Email Flow

**Monday 8:00 AM**
📧 Weekly Summary arrives
- Review last week's performance
- See all pending items
- Plan the week

**Tuesday 8:00 AM** (if 2 days since last digest)
📧 Alternate Day Digest
- Focus on High/Urgent items
- Prioritize your day

**Wednesday (item deadline in 4 days)**
📧 Deadline Alert
- Individual email for specific item
- Take action or delegate

**Thursday (you complete a task)**
📧 Completion Celebration 🎉
- Motivation boost
- See your progress

**Friday (you update status via app)**
📧 Status Change Notification
- Confirmation of update
- Keep track of changes

---

## 🔐 Security Reminder

- ✅ Use App Passwords, not regular password
- ✅ Enable 2FA on Gmail
- ✅ Never share app password
- ✅ Store only in Streamlit secrets
- ✅ Rotate passwords every 3-6 months

---

## 🎯 Success Metrics

**After 1 Week:**
- [ ] Received 2-3 alternate digests
- [ ] Received 1 weekly summary
- [ ] Received deadline alerts (if applicable)
- [ ] Successfully replied to update status
- [ ] No emails in spam

**After 1 Month:**
- [ ] Completion rate increased
- [ ] Never missed a deadline
- [ ] Actively using reply feature
- [ ] Team members also receiving emails
- [ ] Improved productivity

---

## 📞 Support

**Email Issues:**
- Check EMAIL_SETUP_GUIDE.md
- Review Streamlit app logs
- Verify Gmail app password

**Feature Requests:**
- Email timing changes
- Custom email templates
- Additional triggers

---

**Keep this card handy for quick reference! 📧✨**

Print and stick near your desk for easy access to email commands and schedules!
