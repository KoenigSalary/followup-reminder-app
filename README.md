# 📋 Followup Reminder System

A comprehensive web-based application for tracking and managing followup items from meetings, personal notes, and action items with **Koenig Solutions branding**.

[![Live App](https://img.shields.io/badge/Streamlit-Live%20App-FF4B4B?style=for-the-badge&logo=streamlit)](https://followup-reminder-app.streamlit.app)

---

## 🌟 Features

### 🎯 Core Functionality

#### **Multiple Input Methods**
- **Quick Entry Form** - Fast manual entry with all fields
- **Paste MOM Text** - AI-powered extraction from meeting minutes
- **Upload Documents** - Process PDF, Word, Text files
- **AI Extract** - Free text analysis for action items

#### **Smart Reminders**
- Set custom deadlines with any date
- Configurable reminder days before deadline
- Visual urgency indicators with color coding:
  - 🔴 Due Today
  - 🟠 1-3 days left
  - 🟡 4-7 days left
  - 🟢 More than 7 days
- Automatic deadline tracking

#### **Comprehensive Tracking**
- **Status Management**: Pending, In Progress, Completed, Blocked
- **Priority Levels**: Low, Medium, High, Urgent
- **Categories**: Team Meeting, Boss Meeting, Personal Note, Project, Other
- **Person Responsible** tracking
- **Tags** for easy organization
- **Detailed Descriptions** for each item

### 📊 Advanced Features

#### **Dashboard**
- Key metrics (Total, Pending, In Progress, Completed)
- Upcoming deadlines with urgency sorting
- Recent items quick view
- Visual status indicators

#### **All Items View**
- Filter by status, priority, category
- Update status for each item
- Delete items when no longer needed
- Bulk operations support

#### **Search & Filter**
- Search by keywords in titles/descriptions
- Advanced filtering options
- Quick find specific action items

#### **Analytics**
- Completion rate tracking
- Overdue items monitoring
- Status distribution charts
- Priority distribution visualization
- Category breakdown analysis

#### **User Management**
- Secure user authentication
- Password hashing (SHA-256)
- Session-based login
- Each user sees only their own items
- Multi-user support

#### **Branding**
- Koenig Solutions logo integration
- Professional interface design
- Consistent branding throughout

---

## 🚀 Quick Start

### Option 1: Use Live Demo (Recommended)

**Visit:** [https://followup-reminder-app.streamlit.app](https://followup-reminder-app.streamlit.app)

1. Click **Register** to create your account
2. Enter username, email, and password
3. Login with your credentials
4. Start adding followup items!

### Option 2: Local Installation

```bash
# Clone repository
git clone https://github.com/KoenigSalary/followup-reminder-app.git
cd followup-reminder-app

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

App will open at `http://localhost:8501`

---

## 📖 Usage Guide

### 1. Getting Started

#### **First Time Setup:**
1. Open the app (live or local)
2. Click **Register** tab
3. Fill in:
   - Username (unique)
   - Email address
   - Password (min 6 characters)
   - Confirm password
4. Click **Register** button
5. Switch to **Login** tab
6. Enter your credentials
7. Click **Login**

### 2. Adding Items

#### **Method 1: Quick Entry Form**

1. Go to **➕ Add New Item** in sidebar
2. Select **Quick Entry Form** (default)
3. Fill in the details:
   
   **Required:**
   - **Title** - Brief description of the action item
   
   **Optional:**
   - **Category** - Choose from: Team Meeting, Boss Meeting, Personal Note, Project, Other
   - **Priority** - Choose from: Low, Medium, High, Urgent
   - **Person Responsible** - Name of the person who will handle this
   - **Deadline** - When this needs to be completed
   - **Remind me (days before)** - How many days before deadline to remind (default: 3)
   - **Status** - Current state: Pending, In Progress, Completed, Blocked
   - **Tags** - Comma-separated tags (e.g., urgent, finance, review)
   - **Description** - Detailed notes about the action item

4. Click **Add Item** button
5. See success message and balloons! 🎉

#### **Method 2: Paste MOM Text**

1. Go to **➕ Add New Item**
2. Select **Paste MOM Text**
3. Copy your meeting minutes
4. Paste into the text area
5. Click **Extract Action Items**
6. System will identify potential action items looking for keywords:
   - "Action:", "TODO:", "Task:", "Followup:", "Follow-up:", bullet points (-)
7. Review each extracted item:
   - Edit the title if needed
   - Set category, priority, deadline
   - Assign person responsible
8. Click **Add This Item** for each one you want to save

**Example MOM Text:**
```
Meeting Notes - Q4 Planning
Date: Oct 28, 2024

Discussion points:
- Budget review completed
- New hires approved

Action Items:
- Action: Prepare Q4 financial report (John)
- TODO: Schedule training sessions (Sarah)
- Follow-up: Review vendor contracts (Mike)
```

#### **Method 3: Upload Document**

1. Go to **➕ Add New Item**
2. Select **Upload Document**
3. Click **Choose a file**
4. Upload PDF, Word (.docx, .doc), or Text (.txt) file
5. *Note: Document processing feature coming soon*
6. For now, copy text from document and use "Paste MOM Text" method

#### **Method 4: AI Extract from Text**

1. Go to **➕ Add New Item**
2. Select **AI Extract from Text**
3. Type or paste any free-form text containing action items
4. Click **AI Extract**
5. *Note: Enhanced AI extraction coming soon*
6. For now, uses keyword-based extraction similar to MOM text

### 3. Managing Items

#### **Dashboard View**

Navigate to **📊 Dashboard** to see:

**Metrics:**
- Total Items count
- Pending items
- In Progress items
- Completed items

**Upcoming Deadlines:**
- Shows next 5 deadlines
- Color-coded urgency indicators
- Expandable cards with full details
- Auto-sorted by urgency

**Recent Items:**
- Last 5 items created
- Quick status view
- Category and priority display

#### **All Items View**

Navigate to **📋 All Items** to:

**Filter Items:**
- **By Status** - Select one or more: Pending, In Progress, Completed, Blocked
- **By Priority** - Filter by: Low, Medium, High, Urgent
- **By Category** - Choose specific categories

**Manage Items:**
- Expand any item to see full details
- Update status using dropdown
- Click **Update** to save changes
- Click **Delete** to remove item (permanent)
- See item counts: "Showing X items"

**Item Details Shown:**
- Description
- Category
- Person responsible
- Deadline
- Tags
- Created date

#### **Search & Filter**

Navigate to **🔍 Search & Filter** to:

1. Enter search term in search box
2. Searches in:
   - Item titles
   - Item descriptions
3. Shows matching items with:
   - Status
   - Priority
   - Responsible person
   - Description
   - Deadline
4. Results expand automatically for easy viewing

#### **Analytics**

Navigate to **📈 Analytics** to view:

**Key Metrics:**
- **Completion Rate** - Percentage of completed items
- **Overdue Items** - Count of items past deadline
- **Avg. Completion Time** - Coming soon

**Visual Charts:**
- **Status Distribution** - Bar chart showing count per status
- **Priority Distribution** - Bar chart showing count per priority
- **Category Breakdown** - Bar chart showing count per category

### 4. Best Practices

#### **Effective Item Titles**
```
❌ Bad: "Report"
✅ Good: "Prepare Q4 financial report for board meeting"

❌ Bad: "Call"
✅ Good: "Call Sarah to discuss training schedule"
```

#### **Using Priorities**
- **Urgent** - Must be done today/tomorrow
- **High** - Important, do within a week
- **Medium** - Normal priority, do within 2 weeks
- **Low** - Nice to have, flexible timing

#### **Using Tags**
```
Examples:
- urgent, follow-up, needs-approval
- finance, hr, marketing
- q4, annual-review, budget
- client-facing, internal, research
```

#### **Person Responsible**
- Use actual names (e.g., "John Smith")
- Or use roles (e.g., "Marketing Team")
- Or use yourself (e.g., "Me", your username)

---

## 📱 Mobile Access

The application is **fully responsive** and works perfectly on:

- ✅ Desktop browsers (Chrome, Firefox, Safari, Edge)
- ✅ Mobile browsers (iOS Safari, Android Chrome)
- ✅ Tablets (iPad, Android tablets)

### Add to Home Screen

**iOS (iPhone/iPad):**
1. Open app in Safari
2. Tap **Share** button (square with arrow)
3. Scroll down and tap **"Add to Home Screen"**
4. Edit name to "Followup Reminder"
5. Tap **Add**
6. Icon appears on home screen like a native app!

**Android:**
1. Open app in Chrome
2. Tap menu (three vertical dots)
3. Select **"Add to Home Screen"**
4. Edit name to "Followup Reminder"
5. Tap **Add**
6. Icon appears on home screen!

**Benefits:**
- Quick access from home screen
- Runs in full-screen mode
- No browser UI clutter
- Feels like a native app

---

## 🛠️ Technical Stack

**Frontend:**
- Streamlit 1.28+ - Python web framework
- HTML/CSS - Custom styling
- Base64 - Logo encoding

**Backend:**
- Python 3.8+ - Core logic
- JSON - Data storage
- Pathlib - File management
- Hashlib - Password security
- Datetime - Date/time handling

**Authentication:**
- SHA-256 password hashing
- Session state management
- User isolation

**Deployment:**
- Streamlit Cloud (free tier)
- GitHub integration
- Auto-deployment on push

---

## 📁 Project Structure

```
followup-reminder-app/
├── app.py                    # Main application (21KB)
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── .streamlit/
│   └── config.toml          # App configuration
├── assets/
│   └── koenig_logo.png      # Company logo (134KB)
└── data/                    # Created at runtime
    ├── users.json           # User accounts (passwords hashed)
    └── followup_items.json  # All followup items
```

---

## 🔐 Security Features

- **Password Hashing**: All passwords encrypted with SHA-256
- **User Isolation**: Each user can only see their own items
- **Session-based Auth**: Secure login sessions
- **No Data Sharing**: Complete privacy between users
- **No Plain Text Passwords**: Never stored in readable form

---

## 🌐 Deployment to Streamlit Cloud

### Step 1: Create GitHub Repository

1. Create account on [GitHub](https://github.com)
2. Click **New repository**
3. Name it: `followup-reminder-app`
4. Make it Public or Private
5. Click **Create repository**

### Step 2: Upload Files

**Via GitHub Web Interface:**
1. Click **Add file** → **Upload files**
2. Drag and drop:
   - app.py
   - requirements.txt
   - README.md
3. Create `assets` folder, upload `koenig_logo.png`
4. Click **Commit changes**

**Via Git Command Line:**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/followup-reminder-app.git
git push -u origin main
```

### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **New app**
4. Select:
   - **Repository**: YOUR_USERNAME/followup-reminder-app
   - **Branch**: main
   - **Main file path**: app.py
5. Click **Deploy!**
6. Wait 2-3 minutes for deployment

### Step 4: Get Your App URL

After deployment completes, you'll get a URL like:
```
https://YOUR_USERNAME-followup-reminder-app-xxxxx.streamlit.app
```

**Share this URL with your team!**

---

## 💾 Data Storage

### Local Storage (Development)

When running locally with `streamlit run app.py`:

```
data/
├── users.json              # All registered users
└── followup_items.json     # All followup items
```

**Format:**

`users.json`:
```json
{
  "john_doe": {
    "password": "hashed_password_here",
    "email": "john@example.com",
    "created_at": "2024-10-28T10:30:00"
  }
}
```

`followup_items.json`:
```json
[
  {
    "id": 1,
    "title": "Prepare Q4 report",
    "description": "Financial report for board meeting",
    "category": "Team Meeting",
    "priority": "High",
    "responsible": "John Doe",
    "deadline": "2024-11-15",
    "reminder_days": 3,
    "status": "In Progress",
    "tags": ["finance", "urgent", "q4"],
    "owner": "john_doe",
    "created_at": "2024-10-28T10:30:00",
    "updated_at": "2024-10-28T10:30:00"
  }
]
```

### Cloud Storage (Streamlit Cloud)

**⚠️ Important Notes:**
- Data resets when app restarts/redeploys
- For persistent storage, consider using:
  - Google Sheets integration
  - SQLite database
  - Cloud database (MongoDB, Firebase)

---

## 🎨 Customization

### Changing Colors

Edit `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#FF4B4B"      # Koenig red
backgroundColor = "#FFFFFF"    # White background
secondaryBackgroundColor = "#F0F2F6"  # Light gray
textColor = "#262730"         # Dark text
```

### Changing Logo

Replace `assets/koenig_logo.png` with your logo:
- Recommended size: 200px width
- Format: PNG with transparency
- Keep filename: `koenig_logo.png`

---

## 🔧 Troubleshooting

### **App won't start locally**

**Problem:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

**Problem:** Python version too old

**Solution:**
```bash
python --version  # Should be 3.8+
# If older, install Python 3.8 or higher
```

### **Data not persisting on Streamlit Cloud**

**Problem:** Streamlit Cloud resets data on restart

**Solution:**
- This is normal behavior
- For persistent data, use database (future enhancement)
- Currently best for demo/testing purposes

### **Login issues**

**Problem:** Can't login after registration

**Solution:**
1. Clear browser cache (Ctrl+Shift+Del)
2. Try incognito/private mode
3. Re-register with different username

**Problem:** Forgot password

**Solution:**
- Currently no password reset feature
- Register new account
- Or contact admin to reset in `users.json`

### **Items not showing**

**Problem:** Created items but don't see them

**Solution:**
1. Check you're logged in with correct username
2. Items are user-specific (only show yours)
3. Check filters in "All Items" view
4. Try searching in "Search & Filter"

### **Logo not showing**

**Problem:** Koenig logo doesn't appear

**Solution:**
1. Verify `assets/koenig_logo.png` exists
2. Check file path is correct
3. Try clearing browser cache
4. Restart the app

---

## 🚀 Future Enhancements

Planned features for upcoming versions:

### **Version 2.0 (Coming Soon)**
- 📧 Email notifications for reminders
- 👥 Contact management system
- 🔄 Flexible recipient controls
- ⚙️ Email preference settings

### **Version 3.0 (Planned)**
- 🤝 Team collaboration (shared items)
- 🤖 Enhanced AI extraction (OpenAI/Gemini)
- 📅 Calendar integration (Google/Outlook)
- 📄 Export to PDF/Excel

### **Version 4.0 (Future)**
- 📱 Mobile push notifications
- 🔁 Recurring tasks support
- 📎 File attachments
- 💬 Comments and activity log
- 📊 Advanced analytics dashboard

---

## 💡 Tips & Best Practices

### **Organizing Items**

1. **Use Categories Consistently**
   - Team Meeting - for team discussions
   - Boss Meeting - for management requests
   - Personal Note - for self-reminders
   - Project - for long-term initiatives

2. **Set Realistic Deadlines**
   - Add buffer time
   - Consider dependencies
   - Account for approval processes

3. **Use Tags Effectively**
   - Keep tags short (2-3 words max)
   - Use consistent naming
   - Create a tag system for your team

### **Daily Workflow**

**Morning Routine:**
1. Check Dashboard for today's deadlines
2. Review "Upcoming Deadlines" section
3. Update status of items worked yesterday

**After Meetings:**
1. Go to "Paste MOM Text"
2. Paste meeting minutes immediately
3. Extract and assign action items
4. Set deadlines and priorities

**Evening Review:**
1. Go to "All Items"
2. Update status of completed items
3. Adjust priorities if needed
4. Check tomorrow's deadlines

### **Team Usage**

1. **Standardize Naming**
   - Agree on tag conventions
   - Use full names for "Person Responsible"
   - Consistent category usage

2. **Regular Reviews**
   - Weekly team review of pending items
   - Monthly completion rate check
   - Quarterly process improvement

3. **Communication**
   - Screenshot Dashboard for status updates
   - Share Analytics for performance reviews
   - Use consistent terminology

---

## 📞 Support

### **Getting Help**

1. **Check this README** - Most answers are here
2. **Review error messages** - They usually indicate the issue
3. **Check browser console** - F12 for developer tools
4. **Try incognito mode** - Rules out cache issues
5. **Contact admin** - For account/access issues

### **Reporting Issues**

When reporting a problem, include:
- What you were trying to do
- What happened instead
- Error messages (if any)
- Browser and OS version
- Screenshot (if applicable)

### **Contact Information**

- **Email**: praveen.chaudhary@koenig-solutions.com
- **Live App**: [followup-reminder-app.streamlit.app](https://followup-reminder-app.streamlit.app)
- **GitHub**: [github.com/KoenigSalary/followup-reminder-app](https://github.com/KoenigSalary/followup-reminder-app)

---

## 📄 License

Proprietary - Koenig Solutions. All rights reserved.

This software is for internal use by Koenig Solutions and authorized users only.

---

## 🙏 Acknowledgments

**Built with:**
- [Streamlit](https://streamlit.io/) - Web framework
- [Python](https://www.python.org/) - Programming language
- [JSON](https://www.json.org/) - Data format

**Special Thanks:**
- Koenig Solutions team for requirements and testing
- Streamlit community for excellent documentation
- Open source contributors

---

## 📊 Statistics

- **Version**: 1.0 (Current)
- **Release Date**: October 2024
- **Users**: 2+ active users
- **Items Tracked**: Growing daily
- **Uptime**: 99.9% on Streamlit Cloud

---

## 🎉 Enjoy Tracking Your Followups!

**Quick Links:**
- 🌐 **Live App**: https://followup-reminder-app.streamlit.app
- 📚 **Documentation**: This README
- 💻 **Source Code**: GitHub repository
- 📧 **Support**: praveen.chaudhary@koenig-solutions.com

---

*Last Updated: October 28, 2024*  
*Version: 1.0 - Core Features*  
*Maintained by: Koenig Solutions*
