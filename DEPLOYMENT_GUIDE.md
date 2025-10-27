# 🚀 Deployment Guide - Followup Reminder System

This guide will help you deploy your Followup Reminder app so you can share it with your team and access it from anywhere.

## Option 1: Streamlit Cloud (Recommended - FREE) ⭐

### Why Streamlit Cloud?
- ✅ 100% Free for public apps
- ✅ Easy deployment (5 minutes)
- ✅ Automatic HTTPS
- ✅ Share via simple URL
- ✅ No server management needed
- ✅ Works on all devices (iOS, Android, Desktop)

### Step-by-Step Deployment

#### Step 1: Create GitHub Account (if you don't have one)
1. Go to [github.com](https://github.com)
2. Click "Sign up"
3. Follow the registration process

#### Step 2: Upload Your Code to GitHub

**Method A: Using GitHub Web Interface (Easiest)**
1. Login to GitHub
2. Click "+" → "New repository"
3. Name it: `followup-reminder-app`
4. Select "Public" (required for free tier)
5. Click "Create repository"
6. Click "uploading an existing file"
7. Drag and drop all files:
   - `app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `.streamlit/config.toml`
8. Click "Commit changes"

**Method B: Using Git Commands** (if you know Git)
```bash
cd followup_reminder_app
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/followup-reminder-app.git
git push -u origin main
```

#### Step 3: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click "Sign in with GitHub"
3. Authorize Streamlit to access your repositories
4. Click "New app"
5. Fill in details:
   - **Repository**: `YOUR_USERNAME/followup-reminder-app`
   - **Branch**: `main` (or `master`)
   - **Main file path**: `app.py`
   - **App URL** (optional): Choose custom name like `followup-reminder`
6. Click "Deploy!"

#### Step 4: Wait for Deployment
- Takes 2-5 minutes
- You'll see logs showing the deployment progress
- Once done, your app is live!

#### Step 5: Get Your Share Link
Your app will be available at:
```
https://YOUR_USERNAME-followup-reminder-app.streamlit.app
```
or
```
https://share.streamlit.io/YOUR_USERNAME/followup-reminder-app/app.py
```

#### Step 6: Share with Your Team
- Copy the URL
- Send to team members and your boss
- They can bookmark it
- They can add to home screen on mobile

### Important Notes for Streamlit Cloud

**Data Persistence:**
- Current app uses JSON files for storage
- On Streamlit Cloud, files may be lost on app restart
- For production, consider upgrading to database (see below)

**App Sleeping:**
- Free tier apps "sleep" after inactivity
- First load after sleep takes 10-20 seconds
- Subsequent loads are instant

**Resource Limits:**
- Free tier: 1 GB RAM, 1 CPU
- Sufficient for small teams (10-50 users)

---

## Option 2: Deploy with Database (For Persistence)

To prevent data loss on restarts, use a database instead of JSON files.

### Using Supabase (Free PostgreSQL Database)

1. **Create Supabase Account**
   - Go to [supabase.com](https://supabase.com)
   - Sign up for free
   - Create new project

2. **Get Database Credentials**
   - Copy the connection string
   - Save API keys

3. **Update Your App**
   - Modify `app.py` to use Supabase instead of JSON
   - Add Supabase library to `requirements.txt`
   ```
   supabase==1.0.0
   ```

4. **Add Secrets to Streamlit**
   - In Streamlit Cloud dashboard
   - Go to App Settings → Secrets
   - Add your Supabase credentials:
   ```toml
   [supabase]
   url = "your-project-url"
   key = "your-api-key"
   ```

---

## Option 3: Deploy on Your Own Server

### Using Railway.app (Easy, Free Tier Available)

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway auto-detects Streamlit
6. Click "Deploy"
7. Get your public URL

### Using Heroku (Popular Option)

1. Create Heroku account
2. Install Heroku CLI
3. Create additional files:

**Procfile:**
```
web: sh setup.sh && streamlit run app.py
```

**setup.sh:**
```bash
mkdir -p ~/.streamlit/
echo "[server]
headless = true
port = $PORT
enableCORS = false
" > ~/.streamlit/config.toml
```

4. Deploy:
```bash
heroku login
heroku create followup-reminder-app
git push heroku main
heroku open
```

---

## Option 4: Run on Your Computer (Local Network)

For team members on same network:

1. Find your local IP address:
   - Windows: `ipconfig` → Look for IPv4
   - Mac/Linux: `ifconfig` → Look for inet

2. Run app with network access:
```bash
streamlit run app.py --server.address 0.0.0.0
```

3. Share your local URL with team:
```
http://YOUR_IP_ADDRESS:8501
```

**Note**: Only works when your computer is on and on same network.

---

## Choosing the Right Option

| Option | Best For | Pros | Cons |
|--------|----------|------|------|
| **Streamlit Cloud** | Most users | Free, easy, accessible anywhere | Data resets on restart (use database) |
| **Railway/Heroku** | More control | Persistent, professional | Slightly more complex setup |
| **Local Network** | Testing/small teams | Quick setup, private | Only works on same network |
| **Own Server** | Large organizations | Full control | Requires IT knowledge |

## Recommended Setup

### For Your Use Case:
✅ **Streamlit Cloud** (Best choice)
- Quick deployment (5 minutes)
- Free forever
- Share link with team and boss
- Works on all devices
- Later upgrade to Supabase if you need persistence

---

## Mobile Access After Deployment

Once deployed, your team can access on mobile:

### iOS Users:
1. Open URL in Safari
2. Tap Share → "Add to Home Screen"
3. Icon appears like native app

### Android Users:
1. Open URL in Chrome
2. Menu → "Add to Home Screen"
3. Icon appears like native app

---

## Troubleshooting Deployment

### GitHub Upload Issues
- Make sure all files are uploaded
- Check file names match exactly
- Verify no typos in filenames

### Streamlit Cloud Errors
```
ModuleNotFoundError: No module named 'xyz'
```
**Fix**: Add missing module to `requirements.txt`

```
File not found: app.py
```
**Fix**: Ensure `app.py` is in root directory of repo

### App Not Loading
- Check deployment logs in Streamlit Cloud dashboard
- Verify Python version compatibility
- Ensure all dependencies are listed

---

## Updating Your Deployed App

After making changes:

1. Update files on GitHub
2. Streamlit Cloud auto-detects changes
3. Click "Reboot app" in dashboard
4. Changes go live in 1-2 minutes

---

## Security Best Practices

1. **Passwords**: Current app hashes passwords with SHA-256
2. **HTTPS**: Automatically provided by Streamlit Cloud
3. **User Isolation**: Each user only sees their own data
4. **No External Access**: Users can't access other users' items

### For Production:
- Use environment variables for secrets
- Enable two-factor authentication on GitHub
- Regular backups if using database
- Monitor access logs

---

## Next Steps After Deployment

1. ✅ Deploy to Streamlit Cloud
2. ✅ Test with your account
3. ✅ Share URL with 1-2 team members for testing
4. ✅ Gather feedback
5. ✅ Share with entire team and boss
6. ✅ Consider database upgrade if needed

---

## Getting Help

**Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
**Streamlit Forums**: [discuss.streamlit.io](https://discuss.streamlit.io)
**GitHub Issues**: Create issue in your repository

---

**Ready to deploy? Start with Streamlit Cloud - it's the easiest! 🚀**
