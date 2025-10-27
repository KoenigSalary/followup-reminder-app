# ⚡ Quick Start Guide - 5 Minutes to Get Running!

## 🎯 What You'll Get
A web app to track all your followup items from:
- Team meetings MOMs
- Boss meetings MOMs  
- Personal ideas and notes
- With smart reminders and deadlines

## 🚀 Two Options to Get Started

---

### Option 1: Test Locally (2 minutes) 💻

**What you need:**
- Python installed on your computer
- That's it!

**Steps:**
1. **Download all files** to a folder called `followup_reminder_app`

2. **Open terminal/command prompt** and navigate to folder:
   ```bash
   cd path/to/followup_reminder_app
   ```

3. **Install requirements**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

5. **Open in browser**: App opens automatically at `http://localhost:8501`

6. **Start using**:
   - Register your account
   - Add your first followup item
   - Test all features

**Perfect for**: Testing before deploying, personal use, offline access

---

### Option 2: Deploy Online (5 minutes) 🌐

**What you need:**
- GitHub account (free)
- Streamlit account (free)
- Internet connection

**Steps:**
1. **Create GitHub account** at [github.com](https://github.com) (if you don't have)

2. **Create new repository**:
   - Name: `followup-reminder-app`
   - Make it Public
   - Upload all your files

3. **Go to** [share.streamlit.io](https://share.streamlit.io)

4. **Sign in with GitHub** and authorize

5. **Click "New app"** and select:
   - Your repository
   - Main file: `app.py`
   - Click Deploy

6. **Get your link** like: `https://your-name-followup-reminder.streamlit.app`

7. **Share link** with your team!

**Perfect for**: Sharing with team, mobile access, access from anywhere

---

## 📱 After Deployment - Mobile Setup

### Add to iPhone Home Screen:
1. Open link in Safari
2. Tap Share icon (square with arrow)
3. Scroll and tap "Add to Home Screen"
4. Name it "Followups"
5. Now it works like an app!

### Add to Android Home Screen:
1. Open link in Chrome
2. Tap menu (3 dots)
3. Tap "Add to Home Screen"
4. Name it "Followups"
5. Now it works like an app!

---

## 🎓 First Time Usage

### 1. Register Account
- Username: Choose any username
- Email: Your email
- Password: Minimum 6 characters
- Click Register

### 2. Login
- Enter username and password
- Click Login

### 3. Add Your First Item

**Quick Entry:**
- Go to "➕ Add New Item"
- Fill in:
  - Title: "Test followup item"
  - Category: Team Meeting
  - Priority: Medium
  - Deadline: Tomorrow
  - Description: "This is a test"
- Click "Add Item"

### 4. View Dashboard
- Click "📊 Dashboard"
- See your item with deadline
- Check stats

### 5. Try MOM Text Extraction
- Go to "➕ Add New Item"
- Select "Paste MOM Text"
- Paste this example:
  ```
  Meeting Notes - Project Alpha
  Date: Today
  
  Action Items:
  - John to prepare Q4 report by Friday
  - Sarah to review budget and send feedback
  - Team to schedule follow-up meeting next week
  ```
- Click "Extract Action Items"
- Review and add each item

---

## 🔑 Key Features

### Dashboard
- See all your stats at a glance
- Upcoming deadlines with color codes:
  - 🔴 Red = Due today
  - 🟠 Orange = 1-3 days
  - 🟡 Yellow = 4-7 days
  - 🟢 Green = 7+ days

### All Items
- View all followups
- Filter by status, priority, category
- Update status (Pending → In Progress → Completed)
- Delete items

### Search
- Find items quickly
- Search in titles and descriptions

### Analytics
- Completion rate
- Overdue items
- Charts for status, priority, category

---

## 💡 Usage Tips

### For Team Meetings:
1. After meeting, paste MOM text
2. AI extracts action items
3. Assign deadlines
4. Track until completed

### For Boss Meetings:
1. Paste boss's MOM email
2. Extract your action items
3. Set reminders
4. Never miss a deadline!

### For Personal Ideas:
1. Use Quick Entry Form
2. Add idea/note
3. Set timeline for implementation
4. Review in Dashboard

### Best Practices:
- ✅ Set realistic deadlines
- ✅ Update status regularly
- ✅ Use priority levels wisely
- ✅ Add detailed descriptions
- ✅ Review dashboard daily
- ✅ Mark completed items promptly

---

## 🆘 Troubleshooting

### App won't start locally:
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Try running again
streamlit run app.py
```

### Can't login after registration:
- Check username spelling (case-sensitive)
- Try registering with different username
- Clear browser cache

### Deployment failed:
- Verify all files uploaded to GitHub
- Check `requirements.txt` is present
- Wait 2-3 minutes for deployment

### App is slow:
- First load after idle takes 10-20 seconds (normal)
- Subsequent loads are fast
- Consider upgrading to database for better performance

---

## 📚 More Help

- **Full README**: See `README.md` for detailed documentation
- **Deployment Guide**: See `DEPLOYMENT_GUIDE.md` for deployment options
- **Streamlit Docs**: [docs.streamlit.io](https://docs.streamlit.io)

---

## 🎉 You're All Set!

Start tracking your followups and never miss an important action item again!

**Questions?** Check the README or contact your IT team.

---

**Happy Tracking! 🚀**
