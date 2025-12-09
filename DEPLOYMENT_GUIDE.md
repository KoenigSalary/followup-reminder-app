# 🚀 Koenig MoM Agent - Complete Fix & Deployment Guide

## 📋 Issues Fixed

### ✅ Issue #1: OpenAI API Version Error
**Error:** `You tried to access openai.ChatCompletion, but this is no longer supported in openai>=1.0.0`

**Location:** `streamlit_app.py` - TAB 7 (AI MoM Extractor)

**Fix Applied:**
- Changed from old `openai.ChatCompletion.create()` to new `OpenAI()` client
- Updated response parsing from `resp["choices"][0]["message"]["content"]` to `resp.choices[0].message.content`

### ✅ Issue #2: Email Sending Failures
**Problems:**
- Missing `send_email()` function in `mom_agent.py`
- Missing `date` import
- Incomplete email configuration

**Fix Applied:**
- Added complete SMTP email function with error handling
- Added all missing imports
- Added test mode support
- Added proper Excel writing with sheet preservation
- Added escalation functionality

---

## 📂 Files to Replace

### 1. Replace `streamlit_app.py`
**File:** `streamlit_app_FIXED.py`

**Changes:**
- Line ~290: Updated OpenAI API call
- Added `from openai import OpenAI` import
- Changed to new client-based approach

### 2. Replace `mom_agent.py`
**File:** `mom_agent_COMPLETE_FIXED.py`

**Changes:**
- Added complete `send_email()` function with SMTP
- Added `check_overdue_tasks()` function
- Added `escalate_overdue_tasks()` function
- Fixed `add_task()` to preserve Excel sheets
- Added proper date/datetime imports
- Added environment variable support
- Added comprehensive error handling
- Added logging output

---

## 🔧 Step-by-Step Deployment

### Step 1: Update Your GitHub Repository

```bash
# Navigate to your local repo
cd /path/to/followup-reminder-app

# Backup old files (optional but recommended)
cp streamlit_app.py streamlit_app.py.backup
cp mom_agent.py mom_agent.py.backup

# Replace with fixed files
# (Copy the content from streamlit_app_FIXED.py and mom_agent_COMPLETE_FIXED.py)

# Commit changes
git add streamlit_app.py mom_agent.py
git commit -m "Fix OpenAI API v1.0+ compatibility and email sending"
git push origin main
```

### Step 2: Verify GitHub Secrets

Make sure these secrets are set in your GitHub repository:
- Go to: `Settings` → `Secrets and variables` → `Actions`

**Required Secrets:**
```
EMAIL_USER=praveen.chaudhary@koenig-solutions.com
EMAIL_PASS=<your-outlook-app-password>
OPENAI_API_KEY=<your-openai-api-key>
```

**📧 Getting Outlook App Password:**
1. Go to https://account.microsoft.com/security
2. Select "Advanced security options"
3. Under "App passwords", create a new app password
4. Use this password (not your regular password) for `EMAIL_PASS`

### Step 3: Test the Fixes Locally (Optional)

```bash
# Install/upgrade OpenAI package
pip install --upgrade openai>=1.3.0

# Set environment variables
export EMAIL_USER="praveen.chaudhary@koenig-solutions.com"
export EMAIL_PASS="your-app-password"
export OPENAI_API_KEY="your-openai-key"

# Test mom_agent
python mom_agent.py

# Test streamlit dashboard
streamlit run streamlit_app.py
```

### Step 4: Verify GitHub Actions

After pushing:
1. Go to your repo → `Actions` tab
2. Check if workflows run successfully
3. Look for any error messages

**Manual Trigger:**
- Go to `Actions` → Select `MoM Automation Agent` workflow
- Click `Run workflow` → `Run workflow`
- Monitor the run for any errors

---

## 🧪 Testing Checklist

### Email Functionality Test
- [ ] `mom_agent.py` runs without errors
- [ ] Test emails are received at `praveen.chaudhary@koenig-solutions.com`
- [ ] Email subject lines are correct
- [ ] Email body contains task details

### Streamlit Dashboard Test
- [ ] Dashboard loads without errors
- [ ] All 10 tabs are accessible
- [ ] TAB 7 (AI MoM Extractor) works
- [ ] AI extraction completes successfully
- [ ] Extracted tasks can be saved

### GitHub Actions Test
- [ ] Workflow runs on schedule
- [ ] No errors in workflow logs
- [ ] Emails are sent automatically

---

## 🐛 Troubleshooting

### Problem: "Authentication failed" error

**Solution:**
- Use Outlook **App Password**, not your regular password
- Enable 2FA on your Microsoft account first
- Generate a new app password specifically for this app

### Problem: OpenAI API still failing

**Solution:**
```bash
pip uninstall openai
pip install openai==1.12.0
```

### Problem: Excel file not found

**Solution:**
- Ensure `MoM_Master.xlsx` is committed to repo
- Check `config.yaml` path is correct
- Run `python generate_sample_data.py` to create sample data

### Problem: GitHub Actions not running

**Solution:**
- Check if Actions are enabled: `Settings` → `Actions` → `General`
- Verify cron schedule syntax in `.github/workflows/mom_automation.yml`
- Manually trigger workflow to test

---

## 📊 Configuration Reference

### Email Settings (config.yaml)
```yaml
email:
  sender: "praveen.chaudhary@koenig-solutions.com"
  test_mode: true  # Set to false for production
  test_email: "praveen.chaudhary@koenig-solutions.com"
  smtp_server: "smtp.office365.com"
  smtp_port: 587
```

### AI Settings (config.yaml)
```yaml
ai:
  enabled: true
  model: "gpt-4o-mini"  # or "gpt-4o" for better quality
  temperature: 0.0
```

### Escalation Settings (config.yaml)
```yaml
escalation:
  level1_after_days: 2
  level2_after_days: 4
  boss_mom_after_days: 1
  boss_email: "boss@koenig-solutions.com"
```

---

## 🎯 Production Deployment

When ready to go live:

1. **Set `test_mode: false` in `config.yaml`**
   ```yaml
   email:
     test_mode: false  # Real emails to team members
   ```

2. **Update team email addresses in Excel**
   - Open `MoM_Master.xlsx`
   - Update `Users` sheet with real email addresses

3. **Adjust GitHub Actions schedule**
   - Edit `.github/workflows/mom_automation.yml`
   - Set appropriate times for your timezone

4. **Monitor first week**
   - Check Actions logs daily
   - Verify emails are sent correctly
   - Get team feedback

---

## 📞 Support

If you encounter issues:

1. Check GitHub Actions logs for detailed errors
2. Review email server logs (SMTP errors)
3. Test locally with environment variables set
4. Verify all dependencies are installed

---

## ✅ Success Criteria

Your agent is working correctly when:
- ✅ GitHub Actions run on schedule without errors
- ✅ Follow-up emails are sent to team members
- ✅ Streamlit dashboard loads all tabs
- ✅ AI MoM Extractor successfully extracts tasks
- ✅ Overdue tasks are identified and escalated
- ✅ Excel file updates successfully

---

**Built with ❤️ for Koenig Solutions**
