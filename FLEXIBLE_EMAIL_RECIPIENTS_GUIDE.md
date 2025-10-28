# Flexible Email Recipient Control - Implementation Guide

## 🎯 Overview

This feature allows you to control who receives email notifications for each followup item. Previously, emails only went to the item "owner" (creator). Now you can send reminders to the **responsible person** who will actually do the work, while keeping yourself (owner) in the loop.

## ✨ Key Features

### 1. **Send to Responsible Person**
- When creating an item, select who is responsible from dropdown (all registered users)
- Email reminders automatically go to the responsible person
- Perfect for delegating tasks to team members

### 2. **CC Owner (Optional)**
- Checkbox to receive a copy of all emails for the item
- Stay informed while the responsible person gets primary notifications
- Can be enabled/disabled per item

### 3. **Additional Recipients**
- Multi-select to add other people who should receive notifications
- Great for keeping stakeholders informed
- Combines with responsible + owner settings

### 4. **User Email Preferences**
- New "📧 Email Settings" page in navigation
- Master switch to enable/disable all emails
- Per-type controls:
  - 📬 Alternate Day Digest
  - ⚠️ Deadline Alerts
  - 📋 Weekly Summary
  - 🔄 Status Change Notifications
  - 🎉 Completion Celebrations

## 📋 Files Modified/Created

### New Files:
1. **email_preferences.py** ✅ Already in repo
   - Manages user email preferences
   - Handles recipient logic for items
   - Checks if users want specific email types

### Files That Need Updates:
2. **app.py** - Needs enhancement
   - Add "📧 Email Settings" page to navigation
   - Update `quick_entry_form()` to include recipient controls
   - Update `paste_mom_text()` for recipient selection
   - Add `email_settings_page()` function
   - Import `EmailPreferences` class

3. **email_scheduler.py** - Needs enhancement
   - Import `EmailPreferences`
   - Add `get_item_recipients()` method
   - Update `send_alternate_day_digest_job()` to use new recipient logic
   - Update `send_weekly_summary_job()` to use new recipient logic
   - Update `check_deadline_alerts_job()` to use new recipient logic

## 🔧 Implementation Steps

### Step 1: Update app.py

#### Add to imports (line 13):
```python
from email_preferences import EmailPreferences
```

#### Initialize email_preferences (around line 39):
```python
if EMAIL_ENABLED:
    email_service = EmailService()
    email_preferences = EmailPreferences()  # Add this line
```

#### Update navigation in main_app() (around line 173):
```python
page = st.radio(
    "Go to",
    ["📊 Dashboard", "➕ Add New Item", "📋 All Items", 
     "🔍 Search & Filter", "📈 Analytics", "📧 Email Settings"],  # Add Email Settings
    label_visibility="collapsed"
)
```

#### Add elif for Email Settings page (around line 189):
```python
elif page == "📧 Email Settings":
    email_settings_page()
```

#### Add helper functions after load_users():
```python
def get_all_usernames():
    """Get list of all registered usernames"""
    users = load_users()
    return sorted(users.keys())

def get_user_email(username):
    """Get email for a username"""
    users = load_users()
    return users.get(username, {}).get('email')
```

####Update quick_entry_form() function - Add after line 297:
```python
# Change responsible from text_input to selectbox
responsible = st.selectbox(
    "Person Responsible*",
    options=get_all_usernames(),
    help="Select who will be responsible for this task"
)
```

#### Add Email Settings section in quick_entry_form() - Before submitted button:
```python
# Email recipient controls
if EMAIL_ENABLED:
    st.markdown("---")
    st.markdown("### 📧 Email Notification Settings")
    
    col3, col4 = st.columns(2)
    
    with col3:
        send_to_responsible = st.checkbox(
            "Send reminders to Responsible person",
            value=True,
            help="Email notifications will go to the person responsible"
        )
        
        cc_owner = st.checkbox(
            "CC me (Owner) on all emails",
            value=True,
            help="You'll receive a copy of all emails for this item"
        )
    
    with col4:
        additional_recipients = st.multiselect(
            "Also notify (optional):",
            options=[u for u in get_all_usernames() 
                    if u != responsible and u != st.session_state.username],
            help="Select additional people to receive notifications"
        )
    
    # Show summary
    recipients_list = []
    if send_to_responsible:
        recipients_list.append(f"**{responsible}** (Responsible)")
    if cc_owner:
        recipients_list.append(f"**{st.session_state.username}** (Owner - CC)")
    if additional_recipients:
        recipients_list.extend([f"**{r}** (Additional)" for r in additional_recipients])
    
    if recipients_list:
        st.info("📨 Email notifications will be sent to: " + ", ".join(recipients_list))
    else:
        st.warning("⚠️ No email recipients selected!")
```

#### Update the item creation in quick_entry_form() - Modify new_item dict:
```python
# Get email addresses
responsible_email = get_user_email(responsible)
owner_email = get_user_email(st.session_state.username)
additional_emails = [get_user_email(u) for u in additional_recipients] if additional_recipients else []

new_item = {
    'id': len(items) + 1,
    'title': title,
    'description': description,
    'category': category,
    'priority': priority,
    'responsible': responsible,
    'responsible_email': responsible_email,  # Add this
    'deadline': deadline.isoformat(),
    'reminder_days': reminder_days,
    'status': status,
    'tags': [t.strip() for t in tags.split(',') if t.strip()],
    'owner': st.session_state.username,
    'owner_email': owner_email,  # Add this
    'created_at': datetime.now().isoformat(),
    'updated_at': datetime.now().isoformat(),
    # Email settings - Add these
    'send_to_responsible': send_to_responsible if EMAIL_ENABLED else False,
    'cc_owner': cc_owner if EMAIL_ENABLED else False,
    'additional_recipients': additional_emails if EMAIL_ENABLED else []
}
```

#### Add new email_settings_page() function (add anywhere before main execution):
```python
def email_settings_page():
    """Email preferences and settings page"""
    st.title("📧 Email Notification Settings")
    st.markdown("---")
    
    if not EMAIL_ENABLED:
        st.warning("⚠️ Email service is not configured yet.")
        return
    
    st.info("💡 Control which email notifications you receive.")
    
    # Load current preferences
    prefs = email_preferences.get_user_preferences(st.session_state.username)
    
    st.subheader("🔔 Notification Preferences")
    
    with st.form("email_preferences"):
        # Master switch
        email_enabled = st.checkbox(
            "Enable all email notifications",
            value=prefs.get('email_enabled', True),
            help="Turn off to disable all emails"
        )
        
        st.markdown("---")
        st.markdown("### Specific Notification Types")
        
        col1, col2 = st.columns(2)
        
        with col1:
            alternate_digest = st.checkbox(
                "📬 Alternate Day Digest",
                value=prefs.get('alternate_digest', True),
                disabled=not email_enabled
            )
            
            deadline_alerts = st.checkbox(
                "⚠️ Deadline Alerts",
                value=prefs.get('deadline_alerts', True),
                disabled=not email_enabled
            )
            
            weekly_summary = st.checkbox(
                "📋 Weekly Summary",
                value=prefs.get('weekly_summary', True),
                disabled=not email_enabled
            )
        
        with col2:
            status_changes = st.checkbox(
                "🔄 Status Change Notifications",
                value=prefs.get('status_changes', True),
                disabled=not email_enabled
            )
            
            completion_celebration = st.checkbox(
                "🎉 Completion Celebrations",
                value=prefs.get('completion_celebration', True),
                disabled=not email_enabled
            )
        
        st.markdown("---")
        
        if st.form_submit_button("💾 Save Preferences", type="primary"):
            new_prefs = {
                'email_enabled': email_enabled,
                'alternate_digest': alternate_digest,
                'deadline_alerts': deadline_alerts,
                'weekly_summary': weekly_summary,
                'status_changes': status_changes,
                'completion_celebration': completion_celebration
            }
            
            email_preferences.update_user_preferences(st.session_state.username, new_prefs)
            st.success("✅ Email preferences saved successfully!")
```

### Step 2: Update email_scheduler.py

#### Add to imports (line 15):
```python
from email_preferences import EmailPreferences
```

#### Add to __init__ method (around line 19):
```python
def __init__(self):
    self.email_service = EmailService()
    self.email_preferences = EmailPreferences()  # Add this line
    # ... rest of existing code
```

#### Add new method get_item_recipients() (add after load_users method):
```python
def get_item_recipients(self, item, users):
    """
    Get list of recipients for an item based on item settings
    Returns dict with 'all_recipients' list
    """
    recipients = {'all_recipients': []}
    
    owner = item.get('owner')
    responsible = item.get('responsible')
    
    # Primary recipient: responsible person
    if item.get('send_to_responsible', True) and responsible:
        responsible_email = item.get('responsible_email')
        if responsible_email and self.email_preferences.should_send_email(responsible, 'email_enabled'):
            recipients['all_recipients'].append(responsible_email)
    
    # CC owner
    if item.get('cc_owner', True) and owner:
        owner_email = item.get('owner_email')
        if owner_email and self.email_preferences.should_send_email(owner, 'email_enabled'):
            recipients['all_recipients'].append(owner_email)
    
    # Additional recipients
    additional = item.get('additional_recipients', [])
    for email in additional:
        if email not in recipients['all_recipients']:
            recipients['all_recipients'].append(email)
    
    # Fallback to owner if no recipients
    if not recipients['all_recipients'] and owner:
        owner_email = item.get('owner_email')
        if owner_email:
            recipients['all_recipients'].append(owner_email)
    
    return recipients
```

#### Update send_alternate_day_digest_job() - Replace the loop (around line 90):
```python
# Group items by recipient
recipient_items = {}  # email -> list of items

for item in items:
    if item['status'] == 'Completed':
        continue
    
    recipients = self.get_item_recipients(item, users)
    
    for email in recipients['all_recipients']:
        if email not in recipient_items:
            recipient_items[email] = []
        recipient_items[email].append(item)

# Send digest to each recipient
for email, user_items in recipient_items.items():
    # Find username
    username = None
    for uname, udata in users.items():
        if udata.get('email') == email:
            username = uname
            break
    
    if username and not self.email_preferences.should_send_email(username, 'alternate_digest'):
        continue
    
    # Generate and send...
```

## 💡 Usage Examples

### Example 1: Delegate Task to Sarah
1. Login to app
2. Go to "➕ Add New Item"
3. Title: "Prepare Q4 Financial Report"
4. Select **Responsible**: Sarah
5. ✅ Check "Send reminders to Responsible person"
6. ✅ Check "CC me (Owner) on all emails"
7. Add Item

**Result**: Sarah gets all email reminders, you get CC'd

### Example 2: Personal Task (No Delegation)
1. Title: "Review team performance"
2. Select **Responsible**: Yourself
3. ✅ Check "Send reminders to Responsible person"
4. ⬜ Uncheck "CC me" (since you're responsible)

**Result**: Only you receive emails

### Example 3: Multi-Stakeholder Project
1. Title: "Launch new product"
2. Select **Responsible**: ProjectManager
3. ✅ Send to Responsible
4. ✅ CC me
5. **Also notify**: Marketing, Sales, Engineering

**Result**: 5 people receive notifications

## 📧 Email Schedule Reference

- **Alternate Digest**: Every 2 days at 8:00 AM (High/Urgent only)
- **Deadline Alerts**: 4 days before deadline (checked every 6 hours)
- **Weekly Summary**: Every Monday at 8:00 AM (all pending items)
- **Status Changes**: Real-time when status updated
- **Completions**: Real-time celebration email

## 🚀 Testing Checklist

- [ ] Create item with different responsible person
- [ ] Verify responsible person sees email in "Email Settings" would work
- [ ] Test CC owner checkbox
- [ ] Test additional recipients
- [ ] Check Email Settings page loads
- [ ] Save email preferences
- [ ] Create item and verify recipient summary shows correctly
- [ ] Check "All Items" page shows email notification info

## 📝 Notes

- **email_preferences.py** is already in the repo ✅
- **app.py** needs updates (add Email Settings page, recipient controls)
- **email_scheduler.py** needs updates (use new recipient logic)
- All changes are backward compatible
- Existing items without email settings will default to owner

## 🎉 Benefits

1. **True Delegation**: Reminders go to person doing the work
2. **Stay Informed**: Owner can opt-in to receive copies
3. **Team Collaboration**: Multiple people can track same item
4. **Flexible Control**: Per-item and per-user preferences
5. **Reduces Noise**: Each person controls what emails they receive
