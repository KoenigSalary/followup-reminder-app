<p align="center">
  <img src="https://raw.githubusercontent.com/KoenigSalary/followup-reminder-app/54763fec279b95518f17881aedc7099f130dfbcd/koenig_logo.png" width="180" />
</p>

<h2 align="center">Koenig MoM Automation Agent</h2>

---

## 📌 Overview

The **Koenig MoM Automation Agent** is a fully automated meeting follow-up system that:
- Reads MoM points (manual or AI-extracted)
- Tracks tasks across departments
- Sends automated email reminders
- Processes incoming task updates via email replies
- Executes 3-level escalation (Executive → Manager → EA → Boss)
- Stores data in an Excel master file on OneDrive
- Generates daily reports
- Runs independently in cloud via GitHub Actions
- Provides a Streamlit dashboard for visibility & control

This system is built for:
- Accounts/Finance  
- AP/AR  
- HR  
- Sales  
- EA – Director’s Office  
- RMS Team  
- Center Managers  

---

## 🧩 Features

### ✔ MoM Task Management  
- Excel-based master database  
- Department-wise assignment  
- Auto TaskID  
- Status tracking  
- Audit logs  

### ✔ Follow-Up Automation  
Runs **every day** to:
- Send reminders  
- Check deadlines  
- Identify pending/overdue tasks  

### ✔ Email Reply Processing  
Team members can reply:
- “Done”
- “In progress”
- “Need more time”
- “Not my task”

The agent reads the inbox and updates Excel automatically.

### ✔ Escalation Engine  
- Level 1: Executive → Manager  
- Level 2: Manager → EA Office  
- Level 3: EA → Boss (Boss-MoM tasks)  

### ✔ AI MoM Extractor  
Paste meeting notes — AI extracts:
- Action items  
- Assigned persons  
- Deadlines  
- Department  
- Priority  

Automatically creates tasks in Excel.

### ✔ Streamlit Dashboard  
- Overview metrics  
- Task table  
- Boss-MoM view  
- Department dashboard  
- Add task form  
- Escalation log  
- AI extraction GUI  

---

## 📁 File Structure

```
MoM-Agent/
│
├── mom_agent.py
├── streamlit_app.py
├── config.yaml
├── requirements.txt
│
├── assets/
│     └── koenig_logo.png
│
└── .github/
      └── workflows/
            └── mom_automation.yml
```

---

## 🔧 Installation

Clone the repo:

```
git clone https://github.com/KoenigSalary/MoM-Agent.git
cd MoM-Agent
```

Install dependencies:

```
pip install -r requirements.txt
```

Ensure your OneDrive path is correct in `config.yaml`.

---

## ☁️ GitHub Actions Automation

This project includes a workflow that runs:

| Time | Action |
|------|--------|
| 9:00 AM IST | Export daily report |
| 9:30 AM IST | Send reminders |
| 1:00 PM IST | Mid-day reminders |
| 6:00 PM IST | Escalation check |
| Every 30 min | Read inbox + update tasks |

To set up automation, configure **GitHub Secrets**:

| Secret | Value |
|--------|--------|
| EMAIL_USER | your Outlook email |
| EMAIL_PASS | Outlook App Password |
| OPENAI_API_KEY | OpenAI key (optional) |

---

## 🖥 Streamlit Dashboard

Run locally:

```
streamlit run streamlit_app.py
```

---

## 📝 License
Private — For Koenig Solutions internal use only.

---

<p align="center">
  Built with ❤️ for Koenig Solutions
</p>
