# 🚀 Streamlit Cloud Deployment Guide

## Option A: Use GitHub Web Interface (Easiest)

### 1. Create a New GitHub Repository

1. Go to [github.com/new](https://github.com/new)
2. Repository name: `sangeeth-mis-dashboard`
3. Description: "Sangeeth MIS Dashboard - Deployed on Streamlit Cloud"
4. Public (so Streamlit Cloud can access it)
5. Click "Create repository"

### 2. Upload Files to GitHub

1. In your new repo, click **"Add file"** → **"Upload files"**
2. Drag and drop these files:
   - `streamlit_app.py`
   - `requirements.txt`
   - `README.md`
   - `.gitignore`
   - `.streamlit/config.toml` (upload as a folder)

3. Click **"Commit changes"**

### 3. Deploy to Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click **"Sign in"** with your GitHub account
3. Click **"New app"**
4. Fill in:
   - **Repository**: `your-username/sangeeth-mis-dashboard`
   - **Branch**: `main`
   - **Main file**: `streamlit_app.py`
5. Click **"Deploy"**

✅ **Your app is live!** Share the URL with anyone.

---

## Option B: Use Command Line (For Developers)

### 1. Create Local Repo

```bash
cd path/to/your/folder
git init
git add .
git commit -m "Initial commit"
```

### 2. Create GitHub Repo (web)

Go to [github.com/new](https://github.com/new), create empty repo, copy the URL.

### 3. Push to GitHub

```bash
git remote add origin https://github.com/YOUR_USERNAME/sangeeth-mis-dashboard.git
git branch -M main
git push -u origin main
```

### 4. Deploy to Streamlit Cloud

Follow Step 3 from Option A above.

---

## File Organization for GitHub

You'll need these files in your repo:

```
sangeeth-mis-dashboard/
├── streamlit_app.py
├── requirements.txt
├── README.md
├── .gitignore
└── .streamlit/
    └── config.toml
```

---

## 🔑 Setting Credentials (Important!)

### Method 1: Streamlit Cloud Secrets (Recommended)

1. Deploy app to Streamlit Cloud
2. Go to your app → **"Manage app"** (gear icon)
3. Click **"Secrets"**
4. Add:
   ```
   BASE_URL = "http://202.21.37.156/Sangeeth/"
   USERNAME = "SNL4576"
   PASSWORD = "Snl@4576"
   ```
5. Click **"Save"**
6. Update `streamlit_app.py` to read from secrets:

   ```python
   BASE_URL = st.secrets.get("BASE_URL", "http://202.21.37.156/Sangeeth/")
   USERNAME = st.secrets.get("USERNAME", "SNL4576")
   PASSWORD = st.secrets.get("PASSWORD", "Snl@4576")
   ```

### Method 2: Hardcode (Not Recommended - Less Secure)

Leave the credentials in `streamlit_app.py` as they are.

⚠️ **Anyone with access to the GitHub repo will see credentials**

---

## Test Locally First

Before pushing to GitHub:

```bash
pip install -r requirements.txt
playwright install chromium
streamlit run streamlit_app.py
```

Visit `http://localhost:8501` and test.

---

## Share Your Dashboard

Once deployed, you get a shareable link:

```
https://your-app-name.streamlit.app
```

**Share this link with anyone!** No Python installation needed.

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Module not found" | Check `requirements.txt` has all imports |
| "Connection refused" | Verify BASE_URL and credentials |
| "App won't deploy" | Check Streamlit Cloud logs |
| "Very slow loading" | MIS system may be slow; try refreshing |

---

## Update Your App

After deployment, any changes pushed to GitHub auto-deploy:

```bash
# Make changes
nano streamlit_app.py

# Commit and push
git add streamlit_app.py
git commit -m "Update dashboard"
git push origin main
```

Streamlit Cloud redeploys automatically in ~30 seconds!

---

## 🎉 You're Done!

Your Sangeeth MIS Dashboard is now:
- ✅ Live on the web
- ✅ Shareable with a simple link
- ✅ No Python required for users
- ✅ Free hosting (Streamlit Cloud)
- ✅ Auto-updating with new code

Share the link: `https://your-app-name.streamlit.app`

---

**Questions?** Check [Streamlit documentation](https://docs.streamlit.io/)
