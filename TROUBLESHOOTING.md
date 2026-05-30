# 🔧 Streamlit Cloud Troubleshooting Guide

## Error: "Error installing requirements"

### 🎯 Solution (What I Fixed)

I've updated 3 files to fix this:

1. **requirements.txt** - Updated with compatible versions
2. **packages.txt** - Added system dependencies for Linux
3. **streamlit_app.py** - Added automatic Playwright setup

Just download the updated files and re-deploy!

---

## Common Errors & Fixes

### ❌ Error 1: "No module named 'playwright'"

**Cause:** Playwright not installed or version conflict

**Fix:**
```
✅ Delete requirements.txt
✅ Use the updated requirements.txt I provided
✅ Re-deploy on Streamlit Cloud
```

---

### ❌ Error 2: "Failed to launch browser"

**Cause:** Playwright browsers (Chromium) not installed on Streamlit Cloud's Linux servers

**Fix:**
1. Make sure `packages.txt` exists in your repo with system dependencies
2. Make sure `streamlit_app.py` has the subprocess import
3. Delete deployment and re-deploy from scratch

**The updated files already handle this!**

---

### ❌ Error 3: "Connection refused" / "Cannot reach MIS system"

**Cause:** Network connectivity or wrong URL/credentials

**Fix:**

1. **Check BASE_URL is correct:**
   ```python
   BASE_URL = "http://202.21.37.156/Sangeeth/"
   ```

2. **Check credentials are correct:**
   ```python
   USERNAME = "SNL4576"
   PASSWORD = "Snl@4576"
   ```

3. **Use Streamlit Secrets (recommended):**
   - Go to your app on Streamlit Cloud
   - Click gear icon → Secrets
   - Add:
     ```
     BASE_URL = "http://202.21.37.156/Sangeeth/"
     USERNAME = "your-username"
     PASSWORD = "your-password"
     ```

4. **Update streamlit_app.py to read from secrets:**
   ```python
   BASE_URL = st.secrets.get("BASE_URL", "http://202.21.37.156/Sangeeth/")
   USERNAME = st.secrets.get("USERNAME", "SNL4576")
   PASSWORD = st.secrets.get("PASSWORD", "Snl@4576")
   ```

---

### ❌ Error 4: "Timeout" / "App takes too long to load"

**Cause:** Playwright installation takes time, or MIS system is slow

**Fix:**
- First load takes 2-3 minutes (normal!)
- Click "🔄 Refresh Data" to try again
- Check Streamlit Cloud logs for details
- MIS system might be temporarily unavailable

---

### ❌ Error 5: "openpyxl" or "pandas" errors

**Cause:** Version incompatibility

**Fix:**
Use the updated `requirements.txt`:
```
streamlit==1.31.1
playwright==1.40.0
pandas==2.1.4
openpyxl==3.1.2
pyarrow==14.0.1
```

---

## Step-by-Step Fix (If Still Having Issues)

### 1. Update Your GitHub Repo

```bash
# Download the updated files:
# - streamlit_app.py
# - requirements.txt
# - packages.txt (NEW)
# - .gitignore

# Replace old files with new ones

# Push to GitHub
git add .
git commit -m "Fix: Update requirements and dependencies for Streamlit Cloud"
git push origin main
```

### 2. Delete Old Deployment on Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Find your app
3. Click gear icon → "Delete app"
4. Confirm deletion

### 3. Create New Deployment

1. Click **"New app"**
2. Select repo, branch `main`, file `streamlit_app.py`
3. Click **"Deploy"**

### 4. Wait & Monitor Logs

1. Click the 3-dot menu → **"View logs"**
2. Watch for:
   - ✅ "Installing packages..."
   - ✅ "Preparing Playwright browsers..."
   - ✅ "Running streamlit_app.py"

---

## Files You Need in GitHub

```
✅ streamlit_app.py     (MUST HAVE - main app)
✅ requirements.txt     (MUST HAVE - dependencies)
✅ packages.txt         (MUST HAVE - system libs)
✅ .streamlit/config.toml
✅ .gitignore
✅ README.md
```

**If any are missing, that's the problem!**

---

## Local Testing (Optional)

Test locally before deploying:

```bash
# Install dependencies
pip install -r requirements.txt

# Install Playwright
python -m playwright install chromium

# Run app
streamlit run streamlit_app.py
```

If it works locally, it will work on Streamlit Cloud!

---

## Check Streamlit Cloud Logs

**This is the best way to debug:**

1. Go to your app on Streamlit Cloud
2. Click the 3 dots ⋯ (top right)
3. Click **"View logs"**
4. Look for error messages
5. Copy error and search Google

---

## Still Having Issues?

### Option 1: Use Updated Files I Provided
- Download all 7 files from this repo
- Create fresh GitHub repo
- Deploy fresh from Streamlit Cloud

### Option 2: Deploy Locally (Alternative)

If Streamlit Cloud keeps failing, run locally instead:

```bash
pip install -r requirements.txt
python -m playwright install chromium
streamlit run streamlit_app.py
```

Then share with ngrok:
```bash
pip install ngrok
ngrok http 8501
```

Share the public URL!

### Option 3: Simpler Flask Version

Use the Flask version I created earlier (no Playwright needed):
- `flask run`
- Works instantly
- No browser automation issues

---

## What I Fixed in the Updated Files

| File | What Changed | Why |
|------|---|---|
| `requirements.txt` | Updated versions | Better Streamlit Cloud compatibility |
| `packages.txt` | NEW file | System libraries for Playwright on Linux |
| `streamlit_app.py` | Added subprocess import + auto-install Playwright | Handles browser setup automatically |

---

## Quick Checklist

- [ ] Downloaded updated files (7 files total)
- [ ] Created GitHub repo
- [ ] Uploaded ALL 7 files to GitHub (including packages.txt!)
- [ ] Deployed on Streamlit Cloud
- [ ] Clicked "View logs" and checked for errors
- [ ] Waited 2-3 minutes for first load
- [ ] Clicked "🔄 Refresh Data" button
- [ ] Got shareable URL

If all checkmarks, you're good! ✅

---

## Contact Streamlit Support

If nothing works:
- Go to [streamlit.io/cloud](https://streamlit.io/cloud)
- Click "?" → "Ask a question"
- Mention: "Playwright installation fails"
- Attach logs from "View logs"

---

**🎉 You've got this!** Most issues are fixed by using the updated files I provided.
