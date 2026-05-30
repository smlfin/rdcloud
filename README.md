# Sangeeth MIS Dashboard

A modern web-based dashboard for Sangeeth financial MIS reports, deployable to Streamlit Cloud for instant sharing.

## 📊 Features

- **MIS 1**: RD Active Accounts & Instalment tracking
- **MIS 2**: Monthly Closing Report (Payment Collections)
- **MIS 3**: Net for the Month calculation
- **MIS 4**: Deposit Outstanding comparison (month-end vs today)
- **Web-based**: Access from any browser
- **Shareable**: One-click deployment to Streamlit Cloud
- **No Python needed**: For end-users viewing the dashboard

## 🚀 Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit.io account (free)
- This repository

### Step 1: Fork or Clone This Repository

```bash
git clone https://github.com/YOUR_USERNAME/sangeeth-mis-dashboard.git
cd sangeeth-mis-dashboard
```

Or click "Fork" on GitHub.

### Step 2: Deploy to Streamlit Cloud

1. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
2. Click **"New app"**
3. Select:
   - **Repository**: `your-username/sangeeth-mis-dashboard`
   - **Branch**: `main`
   - **Main file path**: `streamlit_app.py`
4. Click **"Deploy"**

That's it! 🎉

Your app will be live at:
```
https://your-app-name.streamlit.app
```

### Step 3: Share the Link

Copy the URL and share with colleagues. They can view it in any browser without installing anything!

---

## 🔧 Local Development

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Install Playwright Browsers

```bash
playwright install chromium
```

### Run Locally

```bash
streamlit run streamlit_app.py
```

Open `http://localhost:8501` in your browser.

---

## ⚙️ Configuration

Edit credentials in `streamlit_app.py`:

```python
BASE_URL = "http://202.21.37.156/Sangeeth/"
USERNAME = "SNL4576"
PASSWORD = "Snl@4576"
```

Or use Streamlit secrets (recommended for cloud):

1. Go to your app settings on Streamlit Cloud
2. Add secrets:
   ```
   BASE_URL = "http://202.21.37.156/Sangeeth/"
   USERNAME = "your-username"
   PASSWORD = "your-password"
   ```
3. Update code:
   ```python
   BASE_URL = st.secrets["BASE_URL"]
   USERNAME = st.secrets["USERNAME"]
   PASSWORD = st.secrets["PASSWORD"]
   ```

---

## 📁 File Structure

```
.
├── streamlit_app.py          # Main Streamlit app
├── requirements.txt          # Python dependencies
├── .streamlit/
│   └── config.toml          # Streamlit configuration
├── .gitignore               # Git ignore rules
└── README.md                # This file
```

---

## 🔄 Updating the App

1. Make changes locally
2. Test with `streamlit run streamlit_app.py`
3. Push to GitHub:
   ```bash
   git add .
   git commit -m "Update dashboard"
   git push origin main
   ```
4. Streamlit Cloud auto-deploys within seconds!

---

## ⏱️ Performance Notes

- **First load**: 2-3 minutes (fetching data)
- **Subsequent loads**: Fast (data cached)
- **Manual refresh**: Click "🔄 Refresh Data" button
- **Timeout**: Streamlit Cloud has 60-minute timeout (sufficient for this app)

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'playwright'"
The dependencies install automatically on Streamlit Cloud. For local development:
```bash
pip install -r requirements.txt
playwright install chromium
```

### "Connection refused"
Check that:
- `BASE_URL` is correct and accessible
- Credentials are valid
- Network/firewall allows connection to the MIS system

### "Timeout during data fetch"
- Remote system may be slow
- Try refreshing again
- Check network connection

### App won't load on Streamlit Cloud
- Check logs: Click "Manage app" → "Logs"
- Verify `streamlit_app.py` exists
- Ensure `requirements.txt` has all dependencies

---

## 📦 Deployment Alternatives

If you prefer not to use Streamlit Cloud:

### Option 1: Deploy to Heroku
```bash
git push heroku main
```
(Requires Heroku account & Procfile)

### Option 2: Run on your server
```bash
python streamlit_app.py
```

### Option 3: Docker
Create a `Dockerfile` and deploy to any container service.

---

## 🔐 Security

⚠️ **Never commit credentials to GitHub**

Use Streamlit Cloud secrets instead:
1. App settings → Secrets
2. Add `BASE_URL`, `USERNAME`, `PASSWORD`
3. Code reads from `st.secrets`

For local dev:
```bash
echo 'BASE_URL = "..."' > .streamlit/secrets.toml
```

---

## 📝 License

Created for Sangeeth workspace.

---

## 💡 Tips

- **Bookmark the URL** for quick access
- **Share with non-technical users** — they just need to click a link
- **Set browser homepage** to your dashboard
- **Add to mobile home screen** on iOS/Android for app-like experience

---

## 🤝 Support

For issues:
1. Check the Streamlit Cloud logs
2. Verify network connection to MIS system
3. Ensure credentials are correct
4. Restart the app (Stop → Rerun on Streamlit Cloud)

---

**Deployed with ❤️ using Streamlit**
