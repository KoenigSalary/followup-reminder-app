# 🔧 Installation Troubleshooting Guide

## Common Installation Issues and Solutions

### Issue 1: Pandas Compilation Error on Mac 🍎

**Error Message:**
```
error: metadata-generation-failed
× Encountered error while generating package metadata.
╰─> pandas
```

**Solution A: Use Pre-built Binaries (Recommended)**
```bash
# Install using conda instead of pip (better for Mac)
conda install streamlit pandas python-dateutil

# Or use pip with pre-built wheels
pip install --only-binary :all: pandas streamlit python-dateutil
```

**Solution B: Use Compatible Versions**
```bash
# Install specific compatible versions
pip install streamlit pandas==1.5.3 python-dateutil
```

**Solution C: Install Without pandas**
The app actually doesn't heavily use pandas! You can run it without:
```bash
# Install only streamlit
pip install streamlit python-dateutil

# Then run the app normally
streamlit run app.py
```

---

### Issue 2: Python Version Compatibility

**Requirements:**
- Python 3.8 or higher
- Python 3.11+ recommended

**Check your Python version:**
```bash
python --version
# or
python3 --version
```

**If version is too old:**
- Download latest Python from [python.org](https://python.org)
- Or use pyenv: `pyenv install 3.11`

---

### Issue 3: Xcode Command Line Tools (Mac)

**If you see compiler errors:**
```bash
xcode-select --install
```

This installs necessary build tools for Mac.

---

### Issue 4: Permission Errors

**If you see "Permission denied":**
```bash
# Use --user flag
pip install --user -r requirements.txt

# Or use virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

---

### Issue 5: Module Not Found After Installation

**If "ModuleNotFoundError" appears:**
```bash
# Make sure you're in the right environment
which python
which pip

# Reinstall in correct environment
pip uninstall streamlit pandas python-dateutil
pip install streamlit pandas python-dateutil
```

---

## Recommended Installation Methods

### Method 1: Conda (Best for Mac/Linux) ⭐
```bash
# Install Miniconda if you don't have it
# Download from: https://docs.conda.io/en/latest/miniconda.html

# Create new environment
conda create -n followup python=3.11
conda activate followup

# Install packages
conda install -c conda-forge streamlit pandas python-dateutil

# Run app
cd followup_reminder_app
streamlit run app.py
```

### Method 2: Virtual Environment with Pip
```bash
cd followup_reminder_app

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# or
venv\Scripts\activate  # Windows

# Install packages
pip install --upgrade pip
pip install streamlit pandas python-dateutil

# Run app
streamlit run app.py
```

### Method 3: System-wide Installation
```bash
# Update pip first
pip install --upgrade pip

# Install packages
pip install streamlit pandas python-dateutil

# Run app
cd followup_reminder_app
streamlit run app.py
```

### Method 4: No pandas Installation
```bash
# Just install streamlit
pip install streamlit python-dateutil

# The app will work fine without pandas!
streamlit run app.py
```

---

## Platform-Specific Solutions

### Mac Issues

**If Homebrew Python:**
```bash
brew install python@3.11
python3.11 -m pip install streamlit pandas python-dateutil
```

**If Apple Silicon (M1/M2/M3):**
```bash
# Use Rosetta or native ARM packages
arch -arm64 pip install streamlit pandas python-dateutil
```

### Windows Issues

**If PowerShell execution policy error:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**If Visual C++ error:**
- Download and install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)

### Linux Issues

**If missing development headers:**
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install python3-dev build-essential

# CentOS/RHEL
sudo yum install python3-devel gcc gcc-c++
```

---

## Quick Fixes Summary

| Error | Quick Fix |
|-------|-----------|
| Pandas won't compile | Use conda OR skip pandas |
| Python too old | Install Python 3.11 |
| Permission denied | Use virtual environment |
| Module not found | Check which python/pip |
| Build tools missing | Install Xcode tools (Mac) |
| Visual C++ error | Install C++ Build Tools (Win) |

---

## Minimal Installation (If All Else Fails)

If you can't get pandas to install, use this minimal setup:

**requirements-minimal.txt:**
```
streamlit>=1.28.0
python-dateutil>=2.8.0
```

**Install:**
```bash
pip install streamlit python-dateutil
```

**Run:**
```bash
streamlit run app.py
```

The app will work perfectly fine without pandas!

---

## Streamlit Cloud Deployment (No Local Installation Needed!)

**Can't install locally? Deploy directly to Streamlit Cloud!**

1. Upload files to GitHub
2. Deploy on [share.streamlit.io](https://share.streamlit.io)
3. Streamlit Cloud handles all dependencies
4. No local installation needed!

**Advantages:**
- ✅ No local installation issues
- ✅ Works from day 1
- ✅ Share with team immediately
- ✅ Access from any device

See **DEPLOYMENT_GUIDE.md** for details.

---

## Still Having Issues?

### Check These:

1. **Python version**: `python --version` (need 3.8+)
2. **Pip version**: `pip --version` (update with `pip install --upgrade pip`)
3. **Virtual environment**: Are you in the right environment?
4. **Disk space**: Do you have enough space?
5. **Internet**: Is your connection stable?

### Get Help:

- **Streamlit Forum**: [discuss.streamlit.io](https://discuss.streamlit.io)
- **Python Help**: [python.org/community](https://python.org/community)
- **Stack Overflow**: Tag your question with `streamlit` and `python`

---

## Alternative: Docker Installation

**If you have Docker:**

Create `Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py"]
```

**Run:**
```bash
docker build -t followup-app .
docker run -p 8501:8501 followup-app
```

---

## Success Checklist

After installation, verify:
- [ ] Python 3.8+ installed
- [ ] Streamlit installed (`streamlit --version`)
- [ ] Can run `streamlit hello` successfully
- [ ] App starts without errors
- [ ] Can register and login
- [ ] Can add items

---

**Need more help? Check the main README.md or DEPLOYMENT_GUIDE.md!**
