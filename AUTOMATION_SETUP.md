# 🤖 Automated CSV Export Setup

**Run the export script automatically every day - NO manual work!**

---

## 🎯 How It Works

1. **Your Computer** (once daily at 8 AM):
   ```
   auto_export.py runs
      ↓
   Fetches data from MIS system
      ↓
   Exports to CSV files
      ↓
   Pushes to GitHub
      ↓
   Streamlit refreshes automatically
   ```

2. **Streamlit Cloud**:
   - Always shows latest data
   - No installation errors
   - No manual work

---

## 📋 Setup Steps

### Step 1: Prepare Your Repo

```
your-repo/
├── streamlit_app.py        (light version)
├── requirements.txt        (light version)
├── auto_export.py          (NEW - automated export)
├── data/
│   ├── mis1.csv
│   ├── mis2.csv
│   └── mis4.csv
└── .github/
    └── workflows/          (GitHub Actions - optional)
```

### Step 2: Install Dependencies

```bash
pip install playwright pandas openpyxl
python -m playwright install chromium
```

### Step 3: Test the Export Script Locally

```bash
python auto_export.py
```

You should see:
```
============================================================
  Sangeeth MIS Data Export
  Started: 2024-05-30 10:30:45
============================================================

🔑 Logging in...
   ✅ Logged in

📋 Fetching MIS 1 (RD Active Accounts)...
   ✅ Exported: data/mis1.csv (1234 rows)

💳 Fetching MIS 2 (Payment Collections)...
   ✅ Exported: data/mis2.csv (567 rows)

📈 Fetching MIS 4 (Deposit Outstanding)...
   ✅ Exported: data/mis4.csv (89 rows)

📤 Pushing to GitHub...
   ✅ Pushed to GitHub

============================================================
✅ Export completed successfully!
   CSVs available in: data/
   Streamlit app auto-reloads on GitHub
============================================================
```

---

## ⏰ Schedule Automatic Runs

### Option A: Windows (Task Scheduler)

1. **Open Task Scheduler**
   - Press `Win + R`
   - Type `taskschd.msc`
   - Press Enter

2. **Create Basic Task**
   - Right-click → "Create Basic Task"
   - Name: `Sangeeth MIS Export`
   - Trigger: `Daily` at `8:00 AM`
   - Action: `Start a program`
   - Program: `python.exe`
   - Arguments: `C:\path\to\auto_export.py`
   - Click OK

3. **Test It**
   - Right-click task → "Run"
   - Check `data/` folder for new CSVs

---

### Option B: Mac/Linux (Cron Job)

1. **Open Terminal**

2. **Edit crontab**
   ```bash
   crontab -e
   ```

3. **Add this line** (runs daily at 8 AM):
   ```
   0 8 * * * cd /path/to/repo && python auto_export.py
   ```

4. **Save** (Ctrl+X, then Y, then Enter)

5. **Verify**
   ```bash
   crontab -l
   ```

---

### Option C: GitHub Actions (Automatic on Cloud)

No need to run on your computer! GitHub runs it for you:

1. **Create this file in repo:**
   ```
   .github/workflows/auto_export.yml
   ```

2. **Add this content:**
   ```yaml
   name: Auto Export MIS Data
   
   on:
     schedule:
       - cron: '0 8 * * *'  # Daily at 8 AM UTC
   
   jobs:
     export:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v3
         
         - name: Set up Python
           uses: actions/setup-python@v4
           with:
             python-version: '3.11'
         
         - name: Install dependencies
           run: |
             pip install playwright pandas openpyxl
             playwright install chromium
         
         - name: Export data
           run: python auto_export.py
         
         - name: Push to GitHub
           run: |
             git config --local user.email "action@github.com"
             git config --local user.name "Auto Export Bot"
             git add data/
             git commit -m "Auto-export $(date +%Y-%m-%d)" || echo "No changes"
             git push
   ```

3. **Push to GitHub**
   - GitHub automatically runs this daily
   - CSVs export automatically
   - Streamlit refreshes automatically
   - **ZERO manual work!** ✅

---

## 🔧 Troubleshooting

### ❌ "Script won't run"
```bash
# Make sure Python is installed
python --version

# Make sure dependencies are installed
pip install playwright pandas openpyxl
python -m playwright install chromium

# Test the script
python auto_export.py
```

### ❌ "Git push fails"
```bash
# Check git config
git config user.name
git config user.email

# Set them
git config --global user.name "Your Name"
git config --global user.email "you@example.com"

# Test push
git push origin main
```

### ❌ "Scheduled task not running"

**Windows:**
- Check Task Scheduler history (right-click task → Properties)
- Make sure Python path is correct
- Try running manually first

**Mac/Linux:**
- Check logs: `log stream --level debug`
- Make sure script has execute permission: `chmod +x auto_export.py`

### ❌ "GitHub Actions won't work"
- Repo must be public (free tier)
- GitHub token auto-generated (you don't need to do anything)
- Check "Actions" tab for logs

---

## 📊 What Gets Exported

| File | Source | Frequency |
|------|--------|-----------|
| `mis1.csv` | MIS 1 - RD Active Accounts | Daily (8 AM) |
| `mis2.csv` | MIS 2 - Payment Collections | Daily (8 AM) |
| `mis4.csv` | MIS 4 - Outstanding Deposits | Daily (8 AM) |

---

## 🎯 Final Setup

### All Together:
1. ✅ `streamlit_app_light.py` → deployed on Streamlit Cloud
2. ✅ `auto_export.py` → scheduled to run daily
3. ✅ `data/*.csv` → auto-updated every day
4. ✅ Streamlit → auto-refreshes when CSVs update

### Result:
- ✅ **Zero manual work**
- ✅ **Automatic data updates**
- ✅ **Always fresh data**
- ✅ **Professional solution**
- ✅ **No installation errors**

---

## 🚀 Recommended Setup

**Best approach for you:**

```
GitHub Actions (Easiest)
├── No local computer needed
├── Runs automatically on GitHub's servers
├── Free tier works fine
└── CSVs update daily automatically
```

**If GitHub Actions fails:**

```
Windows Task Scheduler
├── Runs on your computer
├── Simple GUI setup
├── Reliable
└── Data updates daily
```

---

## 📝 Next Steps

1. Download `auto_export.py`
2. Choose scheduling method:
   - **Option A:** Windows Task Scheduler (easy)
   - **Option B:** Cron Job Mac/Linux (easy)
   - **Option C:** GitHub Actions (easiest, recommended)
3. Test locally: `python auto_export.py`
4. Set up schedule
5. Deploy Streamlit Cloud with light version
6. **Done! Everything runs automatically!** 🎉

---

## 🎊 You Now Have:

- ✅ **CSV Version** (light) for Streamlit Cloud
- ✅ **Auto Export** (scheduled) for daily updates
- ✅ **Zero errors** (no Playwright on cloud)
- ✅ **Fully automated** (no manual work)
- ✅ **Professional** (always fresh data)

**Perfect solution!** 🚀
