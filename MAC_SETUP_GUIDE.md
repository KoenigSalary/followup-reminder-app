# 🍎 Mac Setup Guide - Followup Reminder System

## Complete Setup Guide for Mac Users

---

## 🚀 Quick Start (Choose Your Path)

### Path A: Easiest - Deploy to Streamlit Cloud (Recommended) 🌐
**Skip all installation headaches!**
- No local Python setup needed
- No dependency issues
- Works immediately
- Share with team right away

👉 **Jump to**: [Streamlit Cloud Deployment](#streamlit-cloud-deployment-mac)

---

### Path B: Run Locally on Your Mac 💻
**Test locally before deploying**

👉 **Jump to**: [Local Installation](#local-installation-mac)

---

## 📋 Prerequisites

### Check What You Have:

**1. Python Version**
```bash
python3 --version
```
Need: Python 3.8 or higher (3.11 recommended)

**2. Xcode Command Line Tools** (for pandas)
```bash
xcode-select -p
```
If not found, install:
```bash
xcode-select --install
```

---

## 🌐 Streamlit Cloud Deployment (Mac)

### Why This is Best for Mac:
✅ No local pandas compilation issues  
✅ No Xcode errors  
✅ Works on first try  
✅ Free forever  
✅ Share link with team immediately  

### Step-by-Step:

**1. Download Files from AI Drive**
- All files are in: `/followup_reminder_app/`
- Download entire folder to your Mac

**2. Add Your Koenig Logo**
```bash
# Navigate to downloaded folder
cd ~/Downloads/followup_reminder_app

# Your logo should be at:
# ~/Downloads/followup_reminder_app/assets/koenig_logo.png

# Verify it's there
ls -la assets/koenig_logo.png
```

**3. Create GitHub Account**
- Go to [github.com](https://github.com)
- Sign up (free)

**4. Create New Repository**
- Click "+" → "New repository"
- Name: `followup-reminder-app`
- Make it **Public** (required for free Streamlit)
- Click "Create repository"

**5. Upload Files**

**Option A: GitHub Desktop (Easy for Mac)**
1. Download [GitHub Desktop](https://desktop.github.com/)
2. Clone your repository
3. Copy all files (including `assets` folder with logo)
4. Commit and push

**Option B: GitHub Web Interface**
1. On your repo page, click "uploading an existing file"
2. Drag and drop all files INCLUDING the `assets` folder
3. Make sure `assets/koenig_logo.png` is included
4. Commit changes

**Option C: Terminal (if you know Git)**
```bash
cd ~/Downloads/followup_reminder_app
git init
git add .
git commit -m "Initial commit with Koenig logo"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/followup-reminder-app.git
git push -u origin main
```

**6. Deploy on Streamlit Cloud**
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with GitHub
3. Click "New app"
4. Select: `YOUR_USERNAME/followup-reminder-app`
5. Branch: `main`
6. Main file: `app.py`
7. Click "Deploy"!

**7. Get Your URL**
```
https://YOUR_USERNAME-followup-reminder-app.streamlit.app
```

**8. Share with Team!** 🎉

---

## 💻 Local Installation (Mac)

### Option 1: Using Conda (Recommended for Mac) ⭐

**Why Conda?**
- Pre-compiled binaries (no compilation errors)
- Easier on Mac than pip
- Handles all dependencies smoothly

**Install Miniconda:**
```bash
# Download installer
curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-arm64.sh -o ~/miniconda.sh

# For Intel Macs, use:
# curl https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh -o ~/miniconda.sh

# Install
bash ~/miniconda.sh -b -p $HOME/miniconda

# Initialize
~/miniconda/bin/conda init zsh  # if using zsh
# or
~/miniconda/bin/conda init bash  # if using bash

# Restart terminal
```

**Setup Environment:**
```bash
# Navigate to app folder
cd ~/Downloads/followup_reminder_app

# Create environment
conda create -n followup python=3.11 -y

# Activate
conda activate followup

# Install packages
conda install -c conda-forge streamlit pandas python-dateutil -y
```

**Add Logo:**
```bash
# Run the setup script
./setup_logo.sh

# Or manually verify logo is in place
ls -la assets/koenig_logo.png
```

**Run App:**
```bash
streamlit run app.py
```

App opens at: `http://localhost:8501` 🎉

---

### Option 2: Using Pip (Virtual Environment)

**If you don't want Conda:**

```bash
# Navigate to app folder
cd ~/Downloads/followup_reminder_app

# Create virtual environment
python3 -m venv venv

# Activate
source venv/bin/activate

# Update pip
pip install --upgrade pip

# Install packages (minimal to avoid pandas issues)
pip install streamlit python-dateutil

# Add logo
./setup_logo.sh

# Run app
streamlit run app.py
```

**Note**: If pandas fails to install, the app works fine without it!

---

### Option 3: Homebrew Python

**If using Homebrew:**

```bash
# Install Python via Homebrew
brew install python@3.11

# Navigate to app
cd ~/Downloads/followup_reminder_app

# Create venv with Homebrew Python
/usr/local/opt/python@3.11/bin/python3 -m venv venv

# Activate
source venv/bin/activate

# Install
pip install streamlit python-dateutil

# Setup logo
./setup_logo.sh

# Run
streamlit run app.py
```

---

## 🎨 Koenig Logo Setup

### Quick Setup:

**Automated Script:**
```bash
cd followup_reminder_app
./setup_logo.sh
```

**Manual Setup:**
```bash
# Create assets folder
mkdir -p assets

# Copy logo from Downloads
cp ~/Downloads/followup_reminder_app/assets/koenig_logo.png ./assets/

# Verify
ls -la assets/koenig_logo.png
```

**Where Logo Appears:**
- ✅ Login page (top center)
- ✅ Sidebar (when logged in)

**Customize Logo Size:**
Edit `app.py` and change:
```python
style="max-width: 200px;"  # Change 200 to your preferred size
```

Full guide: See `LOGO_SETUP.md`

---

## 🆘 Troubleshooting (Mac Specific)

### Issue 1: Pandas Compilation Error

**Error:**
```
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> pandas
```

**Solutions:**

**A. Use Conda** (Best)
```bash
conda install -c conda-forge pandas
```

**B. Skip Pandas** (App works without it!)
```bash
pip install streamlit python-dateutil
# Skip pandas entirely
```

**C. Install Xcode Tools**
```bash
xcode-select --install
```

**D. Use Pre-built Wheel**
```bash
pip install --only-binary :all: pandas
```

---

### Issue 2: SSL Certificate Error

**Error:** `SSL: CERTIFICATE_VERIFY_FAILED`

**Fix:**
```bash
# For Python 3.x
cd /Applications/Python\ 3.*/
./Install\ Certificates.command
```

---

### Issue 3: Command Not Found

**Error:** `streamlit: command not found`

**Fix:**
```bash
# Make sure you're in the virtual environment
source venv/bin/activate

# Or use full path
python -m streamlit run app.py
```

---

### Issue 4: Port Already in Use

**Error:** `Port 8501 is already in use`

**Fix:**
```bash
# Kill existing process
pkill -f streamlit

# Or use different port
streamlit run app.py --server.port 8502
```

---

### Issue 5: Logo Not Showing

**Fix:**
```bash
# Check logo exists
ls -la assets/koenig_logo.png

# Check permissions
chmod 644 assets/koenig_logo.png

# Restart app
# Press Ctrl+C, then restart
streamlit run app.py
```

---

## 📱 Mobile Access (iOS)

After deployment:

**Add to iPhone/iPad Home Screen:**
1. Open your deployed URL in Safari
2. Tap Share button (square with arrow up)
3. Scroll and tap "Add to Home Screen"
4. Name it "Followups"
5. Tap "Add"

Now launches like a native app! 📱

---

## 🎯 Recommended Workflow for Mac Users

### Best Practice:

1. ✅ **Download all files** from AI Drive
2. ✅ **Add Koenig logo** (verify it's in `assets/` folder)
3. ✅ **Test locally with Conda** (easiest on Mac)
4. ✅ **Deploy to Streamlit Cloud** (share with team)
5. ✅ **Add to iPhone home screen** (mobile access)

### Time Estimate:
- Conda setup: 5 minutes
- Local testing: 5 minutes
- GitHub upload: 5 minutes
- Streamlit deployment: 5 minutes
- **Total: 20 minutes** ⏱️

---

## 💡 Mac-Specific Tips

### Terminal Tips:
```bash
# Show hidden files in Finder
defaults write com.apple.finder AppleShowAllFiles YES
killall Finder

# Find Python installations
which -a python3

# Check architecture (Intel vs Apple Silicon)
uname -m
# x86_64 = Intel
# arm64 = Apple Silicon (M1/M2/M3)
```

### Performance Tips:
- Use Conda for dependencies (faster on Mac)
- Keep Terminal app updated
- Use latest macOS for best compatibility
- Apple Silicon? Use native ARM Python

---

## 🔗 Quick Links

- **Logo Setup**: `LOGO_SETUP.md`
- **Installation Issues**: `INSTALL_TROUBLESHOOTING.md`
- **Deployment Guide**: `DEPLOYMENT_GUIDE.md`
- **Features**: `FEATURES.md`
- **Quick Start**: `QUICK_START.md`

---

## ✅ Success Checklist

After setup, verify:
- [ ] Python 3.8+ installed
- [ ] Logo file in `assets/koenig_logo.png`
- [ ] Streamlit installed (`streamlit --version`)
- [ ] App runs locally (`streamlit run app.py`)
- [ ] Logo appears on login page
- [ ] Logo appears in sidebar
- [ ] Can register and login
- [ ] Can add followup items

---

## 🎉 You're All Set!

**Local Testing:**
```bash
cd followup_reminder_app
source venv/bin/activate  # or: conda activate followup
streamlit run app.py
```

**Deploy to Cloud:**
See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Need Help?**
Check [INSTALL_TROUBLESHOOTING.md](INSTALL_TROUBLESHOOTING.md)

---

**Happy tracking! Never miss a followup again! 🚀**
