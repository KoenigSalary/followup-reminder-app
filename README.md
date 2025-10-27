# 📋 Followup Reminder System

A comprehensive web-based application for tracking and managing followup items from meetings, personal notes, and action items.

## Features

### 🎯 Core Functionality
- **Multiple Input Methods**
  - Quick entry form
  - Paste Minutes of Meeting (MOM) text with AI extraction
  - Upload documents (PDF, Word, Text)
  - AI-powered extraction from free text

- **Smart Reminders**
  - Set custom deadlines
  - Configurable reminder days before deadline
  - Visual urgency indicators (color-coded)
  - Automatic deadline tracking

- **Comprehensive Tracking**
  - Status management (Pending, In Progress, Completed, Blocked)
  - Priority levels (Low, Medium, High, Urgent)
  - Categories (Team Meeting, Boss Meeting, Personal Note, Project, Other)
  - Person responsible tracking
  - Tags for easy organization

- **Advanced Features**
  - Dashboard with key metrics
  - Upcoming deadlines view
  - Search and filter capabilities
  - Analytics and insights
  - User authentication
  - Persistent data storage

## Installation

### 1. Clone or Download Files
Download all files to your computer:
- `app.py`
- `requirements.txt`
- `README.md`

### 2. Install Python
Make sure you have Python 3.8+ installed:
```bash
python --version
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Deployment to Streamlit Cloud (Free)

### Step 1: Create GitHub Repository
1. Create account on [GitHub](https://github.com)
2. Create new repository (e.g., "followup-reminder-app")
3. Upload all files to the repository

### Step 2: Deploy on Streamlit Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Click "Deploy"

### Step 3: Share Your App
After deployment, you'll get a URL like:
```
https://your-username-followup-reminder-app-app-xxxxx.streamlit.app
```

Share this URL with your team!

## Usage Guide

### First Time Setup
1. **Register Account**: Create your account with username, email, and password
2. **Login**: Use your credentials to access the system

### Adding Items

#### Method 1: Quick Entry Form
1. Go to "➕ Add New Item"
2. Select "Quick Entry Form"
3. Fill in details:
   - Title (required)
   - Category, Priority, Status
   - Person responsible
   - Deadline and reminder days
   - Description and tags
4. Click "Add Item"

#### Method 2: Paste MOM Text
1. Go to "➕ Add New Item"
2. Select "Paste MOM Text"
3. Paste your meeting minutes
4. System extracts action items automatically
5. Review and add each item

#### Method 3: Upload Document
1. Go to "➕ Add New Item"
2. Select "Upload Document"
3. Upload PDF, Word, or text file
4. System processes and extracts action items

### Managing Items

#### Dashboard View
- See total items, pending, in progress, completed
- View upcoming deadlines with urgency indicators
- Check recent items

#### All Items View
- Filter by status, priority, category
- Update status for each item
- Delete items when no longer needed

#### Search & Filter
- Search by keywords in titles/descriptions
- Quick find specific action items

#### Analytics
- View completion rates
- Check overdue items
- Analyze status, priority, and category distributions

## Mobile Access

The application is fully responsive and works on:
- ✅ Desktop browsers (Chrome, Firefox, Safari, Edge)
- ✅ Mobile browsers (iOS Safari, Android Chrome)
- ✅ Tablets

### Add to Home Screen (Mobile)

**iOS (iPhone/iPad):**
1. Open the app URL in Safari
2. Tap the Share button
3. Select "Add to Home Screen"
4. Name it "Followup Reminder"
5. Tap "Add"

**Android:**
1. Open the app URL in Chrome
2. Tap the menu (three dots)
3. Select "Add to Home Screen"
4. Name it "Followup Reminder"
5. Tap "Add"

Now you can launch it like a native app!

## Data Storage

- All data is stored in JSON files in the `data/` directory
- `users.json`: User accounts (passwords are hashed)
- `followup_items.json`: All followup items
- Data persists across sessions
- Each user sees only their own items

## Security

- Passwords are hashed using SHA-256
- Users can only access their own items
- Session-based authentication
- No data shared between users

## Future Enhancements

Planned features:
- Email notifications for reminders
- Team collaboration (shared items)
- Enhanced AI extraction using OpenAI/Gemini
- Calendar integration
- Export to PDF/Excel
- Mobile push notifications
- Recurring tasks
- File attachments
- Comments and activity log

## Troubleshooting

### App won't start
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Run with verbose logging
streamlit run app.py --logger.level=debug
```

### Data not persisting
- Check that `data/` directory exists
- Verify file permissions
- On Streamlit Cloud, data resets on restart (consider using database)

### Login issues
- Clear browser cache
- Try incognito/private mode
- Re-register if needed

## Support

For issues or questions:
1. Check this README
2. Review error messages in the app
3. Check Streamlit logs
4. Verify all files are present

## License

Free to use and modify for personal and commercial purposes.

## Credits

Built with:
- Streamlit (Web framework)
- Python (Backend)
- JSON (Data storage)

---

**Enjoy tracking your followups! 🚀**
