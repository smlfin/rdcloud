# 📋 Sangeeth MIS Dashboard — Quick Reference

## What This Is

A **web-based dashboard** for Sangeeth MIS reports that:
- ✅ Works in any web browser
- ✅ No Python needed to use it
- ✅ Automatically fetches latest data
- ✅ Shareable with colleagues
- ✅ Deployed on free Streamlit Cloud

## 3-Minute Setup

### Step 1: GitHub Account (If you don't have one)
1. Go to [github.com/signup](https://github.com/signup)
2. Sign up with email
3. Verify email

### Step 2: Create GitHub Repo
1. Go to [github.com/new](https://github.com/new)
2. Name: `sangeeth-mis-dashboard`
3. Make it **Public**
4. Click **Create Repository**

### Step 3: Upload Files
1. Click **"Add file"** → **"Upload files"**
2. Upload these 6 items from the files you downloaded:
   - `streamlit_app.py`
   - `requirements.txt`
   - `README.md`
   - `DEPLOY_GUIDE.md`
   - `.gitignore`
   - `.streamlit/config.toml` (file inside a folder)
3. Click **"Commit changes"**

### Step 4: Deploy to Streamlit Cloud
1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click **"Sign in"** (use GitHub)
3. Click **"New app"**
4. Select:
   - Repo: `your-username/sangeeth-mis-dashboard`
   - Branch: `main`
   - File: `streamlit_app.py`
5. Click **Deploy**

### Step 5: Wait for Deployment
- Takes ~2-3 minutes
- You'll see a progress indicator
- Green checkmark = Ready!

### Step 6: Get Your Shareable Link
- Your app is now live at:
  ```
  https://your-app-name.streamlit.app
  ```
- Share this URL with anyone!

---

## The 4 MIS Reports

| Report | Shows |
|--------|-------|
| **MIS 1** | RD Active Accounts & Instalment amounts |
| **MIS 2** | Monthly Payment Collections by company |
| **MIS 3** | Net calculation (MIS 1 - MIS 2) |
| **MIS 4** | Outstanding deposits comparison |

---

## Common Tasks

### 🔄 Update the Dashboard

```bash
# Make changes
nano streamlit_app.py

# Push to GitHub
git add .
git commit -m "Updated dashboard"
git push origin main
```

Auto-deploys in ~30 seconds on Streamlit Cloud!

### 🔑 Change Credentials

Option 1 (Cloud):
1. Go to your app on Streamlit Cloud
2. Click settings (gear icon)
3. Click "Secrets"
4. Add your credentials there

Option 2 (Local):
1. Edit `streamlit_app.py`
2. Change `USERNAME` and `PASSWORD`
3. Commit and push

### 🌍 Access from Anywhere

Just share the Streamlit URL:
```
https://your-app-name.streamlit.app
```

No installation needed for users!

### 📱 Mobile/Tablet Access

The dashboard works on:
- 📱 iPhone / Android
- 📱 iPad / Tablets
- 🖥️ Desktop computers
- 💻 Laptops

Just open the link in any browser!

---

## File Descriptions

| File | Purpose |
|------|---------|
| `streamlit_app.py` | **Main app** - Contains all logic and UI |
| `requirements.txt` | **Dependencies** - Python packages needed |
| `README.md` | **Documentation** - User guide |
| `.gitignore` | **Git config** - Files to ignore in Git |
| `.streamlit/config.toml` | **Streamlit config** - UI customization |
| `DEPLOY_GUIDE.md` | **Deployment steps** - How to deploy |

---

## Troubleshooting

### ❌ "App won't deploy"
- ✅ Check Streamlit Cloud logs
- ✅ Verify `requirements.txt` is correct
- ✅ Make sure `streamlit_app.py` exists

### ❌ "Connection error to MIS system"
- ✅ Check internet connection
- ✅ Verify BASE_URL is correct
- ✅ Verify username/password are correct

### ❌ "Very slow loading"
- ✅ First load takes 2-3 minutes (normal)
- ✅ MIS system may be slow
- ✅ Click "Refresh Data" to retry

### ❌ "Data not showing"
- ✅ Click "🔄 Refresh Data" button
- ✅ Wait for it to complete
- ✅ Check credentials in Streamlit secrets

---

## Security Notes

⚠️ **Keep credentials safe:**
- ❌ Don't commit credentials to GitHub
- ✅ Use Streamlit Cloud Secrets instead
- ✅ Or hardcode in `streamlit_app.py` (less secure)

---

## Getting Help

1. Check the logs on Streamlit Cloud (gear icon → Logs)
2. Read `DEPLOY_GUIDE.md` for detailed steps
3. Check [Streamlit documentation](https://docs.streamlit.io/)

---

## Your Shareable Link

Once deployed, share:

```
https://your-app-name.streamlit.app
```

Anyone with this link can view your dashboard in a browser! 🎉
