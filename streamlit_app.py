#!/usr/bin/env python3
"""
Sangeeth MIS Workspace Controller — Streamlit Dashboard

Fetches and displays:
- MIS 1: RD Active Accounts & Instalment
- MIS 2: Monthly Closing Report (RD Payment Collections)
- MIS 3: Net for the Month (MIS 1 Instalment − MIS 2 Amount)
- MIS 4: Deposit Outstanding Comparison (prev-month-end vs today)

Deploy to Streamlit Cloud from GitHub:
1. Push this repo to GitHub
2. Go to https://streamlit.io/cloud
3. Connect your GitHub account
4. Deploy this app
5. Share the URL!
"""

import streamlit as st
from playwright.sync_api import sync_playwright
from datetime import datetime, date
from calendar import monthrange
import pandas as pd
import threading
import time
import re
import subprocess

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Sangeeth MIS Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ─────────────────────────────────────────────
#  CONFIGURATION
# ─────────────────────────────────────────────

BASE_URL = "http://202.21.37.156/Sangeeth/"
USERNAME = "SNL4576"
PASSWORD = "Snl@4576"

_today            = datetime.today()
_today_str        = _today.strftime("%d/%m/%Y")
_today_date_str   = _today.strftime("%Y%m%d")
FROM_DATE_MONTH   = _today.replace(day=1).strftime("%d/%m/%Y")
FROM_DATE_DETAILS = "01/01/2020"

_d = _today.date()
if _d.month == 1:
    _prev_last = date(_d.year - 1, 12, 31)
else:
    _prev_last = date(_d.year, _d.month - 1, monthrange(_d.year, _d.month - 1)[1])
PREV_MONTH_END_STR = _prev_last.strftime("%d/%m/%Y")


# ─────────────────────────────────────────────
#  INITIALIZE SESSION STATE
# ─────────────────────────────────────────────

if 'df_snap' not in st.session_state:
    st.session_state.df_snap = None
if 'df_payment' not in st.session_state:
    st.session_state.df_payment = None
if 'out_prev' not in st.session_state:
    st.session_state.out_prev = None
if 'out_today' not in st.session_state:
    st.session_state.out_today = None
if 'out_diff' not in st.session_state:
    st.session_state.out_diff = None
if 'out_prev_co' not in st.session_state:
    st.session_state.out_prev_co = {}
if 'out_today_co' not in st.session_state:
    st.session_state.out_today_co = {}
if 'status' not in st.session_state:
    st.session_state.status = "Ready to fetch data"
if 'is_loading' not in st.session_state:
    st.session_state.is_loading = False
if 'error_msg' not in st.session_state:
    st.session_state.error_msg = None
if 'last_updated' not in st.session_state:
    st.session_state.last_updated = None


# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

def normalise_company(raw):
    s = str(raw).strip()
    if not s or s.lower() == "nan":
        return "Unknown"
    if "VFL" in s.upper():
        return "VFL"
    if "SML" in s.upper():
        return "SML"
    if re.match(r"^\d+", s):
        return "SNL"
    return "SNL"


def fill_date(page, label_text, date_value):
    try:
        input_id = page.locator(f"label:has-text('{label_text}')").first.get_attribute("for")
        field = (page.locator(f"#{input_id}") if input_id
                 else page.locator(f"label:has-text('{label_text}')").locator("..").locator("input").first)
        field.evaluate(
            "(el, val) => { el.value = val; el.dispatchEvent(new Event('change', {bubbles:true})); }",
            date_value)
        field.click(click_count=3)
        field.type(date_value)
    except Exception:
        pass


def fill_ason_date(page, date_value):
    try:
        page.evaluate(
            "(val) => {"
            "  const inputs = Array.from(document.querySelectorAll('input[type=text]'));"
            "  if (inputs[0]) {"
            "    inputs[0].value = val;"
            "    inputs[0].dispatchEvent(new Event('change', {bubbles:true}));"
            "  }"
            "}",
            date_value)
    except Exception:
        pass


def locate_export_select(report_page):
    for sel in report_page.locator("select").all():
        try:
            opts = sel.evaluate("el => Array.from(el.options).map(o => o.text)")
            if any("CSV" in o or "Excel" in o for o in opts):
                return sel
        except Exception:
            pass
    for frame in report_page.frames:
        if frame == report_page.main_frame:
            continue
        try:
            for sel in frame.locator("select").all():
                try:
                    opts = sel.evaluate("el => Array.from(el.options).map(o => o.text)")
                    if any("CSV" in o or "Excel" in o for o in opts):
                        return sel
                except Exception:
                    pass
        except Exception:
            pass
    return None


def generate_and_download(context, page, temp_path, export_format="Excel 97-2003"):
    try:
        with context.expect_page(timeout=60000) as npi:
            page.click(
                "button:has-text('Generate'), input[value='Generate'], button:has-text('View Report')",
                timeout=15000)
        rp = npi.value
        rp.wait_for_load_state("networkidle", timeout=60000)
        export_sel = locate_export_select(rp)
        if not export_sel:
            rp.close()
            return False
        export_sel.select_option(label=export_format)
        with rp.expect_download(timeout=90000) as dl_info:
            rp.locator("a[id*='Export'], input[id*='Export'], button[id*='Export']").first.click(
                timeout=10000, no_wait_after=True)
        dl_info.value.save_as(temp_path)
        rp.close()
        return True
    except Exception as e:
        st.session_state.error_msg = f"Download error: {e}"
        return False


def read_xls_file(file_path):
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except Exception:
        return None


# ─────────────────────────────────────────────
#  AUTOMATION FUNCTION
# ─────────────────────────────────────────────

def run_automation():
    """Fetch all MIS data from remote system"""
    try:
        st.session_state.is_loading = True
        st.session_state.error_msg = None
        
        status_placeholder = st.empty()
        
        # Install Playwright browsers if needed (for Streamlit Cloud)
        try:
            import subprocess
            status_placeholder.info("🔧 Preparing Playwright browsers...")
            subprocess.run(
                ["python", "-m", "playwright", "install", "chromium"],
                capture_output=True,
                timeout=120,
                check=False
            )
        except Exception as e:
            pass  # Continue anyway, browsers might already exist
        
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox"])
            context = browser.new_context()
            page = context.new_page()
            
            # Login
            status_placeholder.info("🔑 Logging into system...")
            page.goto(BASE_URL, timeout=60000)
            page.fill("input[name='username']", USERNAME)
            page.fill("input[name='password']", PASSWORD)
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            
            # MIS 1 - RD Active Accounts
            status_placeholder.info("📋 Fetching MIS 1 (RD Active Accounts)...")
            page.goto(f"{BASE_URL}mis1", timeout=60000)
            page.wait_for_load_state("networkidle")
            fill_date(page, "From Date", FROM_DATE_MONTH)
            fill_date(page, "To Date", _today_str)
            
            mis1_file = f"/tmp/mis1_{_today_date_str}.xls"
            if generate_and_download(context, page, mis1_file):
                st.session_state.df_snap = read_xls_file(mis1_file)
            
            # MIS 2 - Payment Collections
            status_placeholder.info("💳 Fetching MIS 2 (Payment Collections)...")
            page.goto(f"{BASE_URL}mis2", timeout=60000)
            page.wait_for_load_state("networkidle")
            fill_date(page, "From Date", FROM_DATE_MONTH)
            fill_date(page, "To Date", _today_str)
            
            mis2_file = f"/tmp/mis2_{_today_date_str}.xls"
            if generate_and_download(context, page, mis2_file):
                st.session_state.df_payment = read_xls_file(mis2_file)
            
            # MIS 4 - Outstanding
            status_placeholder.info("📈 Fetching MIS 4 (Deposit Outstanding)...")
            page.goto(f"{BASE_URL}mis4", timeout=60000)
            page.wait_for_load_state("networkidle")
            fill_ason_date(page, PREV_MONTH_END_STR)
            
            mis4_file = f"/tmp/mis4_prev_{_today_date_str}.xls"
            if generate_and_download(context, page, mis4_file):
                df = read_xls_file(mis4_file)
                if df is not None and "Outstanding" in df.columns:
                    st.session_state.out_prev = df["Outstanding"].sum()
                    if "Company" in df.columns:
                        st.session_state.out_prev_co = dict(zip(df["Company"], df["Outstanding"]))
            
            fill_ason_date(page, _today_str)
            
            mis4_today_file = f"/tmp/mis4_today_{_today_date_str}.xls"
            if generate_and_download(context, page, mis4_today_file):
                df = read_xls_file(mis4_today_file)
                if df is not None and "Outstanding" in df.columns:
                    st.session_state.out_today = df["Outstanding"].sum()
                    if "Company" in df.columns:
                        st.session_state.out_today_co = dict(zip(df["Company"], df["Outstanding"]))
            
            if st.session_state.out_prev is not None and st.session_state.out_today is not None:
                st.session_state.out_diff = st.session_state.out_today - st.session_state.out_prev
            
            browser.close()
            
            st.session_state.status = "Data loaded successfully ✓"
            st.session_state.last_updated = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            status_placeholder.success(f"✓ Data loaded at {st.session_state.last_updated}")
            
    except Exception as e:
        st.session_state.error_msg = str(e)
        st.session_state.status = f"Error: {e}"
    finally:
        st.session_state.is_loading = False


# ─────────────────────────────────────────────
#  UI LAYOUT
# ─────────────────────────────────────────────

def render_dashboard():
    """Render the main dashboard"""
    
    # Header
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        st.title("📊 Sangeeth MIS Dashboard")
        st.caption(f"Real-time financial reporting • Updated: {st.session_state.last_updated or 'Never'}")
    
    with col3:
        if st.button("🔄 Refresh Data", disabled=st.session_state.is_loading, use_container_width=True):
            run_automation()
            st.rerun()
    
    # Error message
    if st.session_state.error_msg:
        st.error(f"⚠️ {st.session_state.error_msg}")
    
    # Loading indicator
    if st.session_state.is_loading:
        st.info("⏳ Fetching data from system... This may take a few minutes.")
    
    # Dashboard
    if st.session_state.df_snap is None and st.session_state.df_payment is None:
        st.warning("👈 Click 'Refresh Data' above to load MIS reports")
        return
    
    # MIS 1 - RD Active Accounts
    st.subheader("▸ MIS 1 — RD Active Accounts & Instalment", divider="blue")
    if st.session_state.df_snap is not None and not st.session_state.df_snap.empty:
        df = st.session_state.df_snap
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Accounts", f"{len(df):,}")
        with col2:
            total = df["Instalment"].sum() if "Instalment" in df.columns else 0
            st.metric("Total Instalment", f"₹ {total:,.2f}")
        
        if "Company" in df.columns and "Instalment" in df.columns:
            summary = (df.groupby("Company")
                      .agg(Count=("Instalment", "count"), Total=("Instalment", "sum"))
                      .reset_index().sort_values("Total", ascending=False))
            
            summary.columns = ["Company", "Accounts", "Instalment Amount"]
            summary["Instalment Amount"] = summary["Instalment Amount"].apply(lambda x: f"₹ {x:,.2f}")
            st.dataframe(summary, use_container_width=True, hide_index=True)
    else:
        st.info("No data available for MIS 1")
    
    # MIS 2 - Payment Collections
    st.subheader("▸ MIS 2 — Monthly Closing Report (Payment Collections)", divider="green")
    if st.session_state.df_payment is not None and not st.session_state.df_payment.empty:
        df = st.session_state.df_payment
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Transactions", f"{len(df):,}")
        with col2:
            total = df["Principal"].sum() if "Principal" in df.columns else 0
            st.metric("Total Principal", f"₹ {total:,.2f}")
        
        if "Company" in df.columns and "Principal" in df.columns:
            summary = (df.groupby("Company")
                      .agg(Count=("Principal", "count"), Total=("Principal", "sum"))
                      .reset_index().sort_values("Total", ascending=False))
            
            summary.columns = ["Company", "Transactions", "Principal Amount"]
            summary["Principal Amount"] = summary["Principal Amount"].apply(lambda x: f"₹ {x:,.2f}")
            st.dataframe(summary, use_container_width=True, hide_index=True)
    else:
        st.info("No data available for MIS 2")
    
    # MIS 3 - Net for Month
    st.subheader("▸ MIS 3 — Net for the Month (MIS 1 Instalment − MIS 2 Amount)", divider="orange")
    
    inst_total = st.session_state.df_snap["Instalment"].sum() if (st.session_state.df_snap is not None and "Instalment" in st.session_state.df_snap.columns) else 0
    amt_total = st.session_state.df_payment["Amount"].sum() if (st.session_state.df_payment is not None and "Amount" in st.session_state.df_payment.columns) else 0
    net_total = inst_total - amt_total
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("MIS 1 Instalment", f"₹ {inst_total:,.2f}")
    with col2:
        st.metric("MIS 2 Amount", f"₹ {amt_total:,.2f}")
    with col3:
        delta = f"{'▲' if net_total >= 0 else '▼'} ₹ {abs(net_total):,.2f}"
        st.metric("Net", delta, delta_color="off")
    
    # MIS 4 - Outstanding
    st.subheader(f"▸ MIS 4 — Deposit Outstanding ({PREV_MONTH_END_STR} vs {_today_str})", divider="red")
    
    prev_val = st.session_state.out_prev
    today_val = st.session_state.out_today
    diff_val = st.session_state.out_diff
    
    col1, col2, col3 = st.columns(3)
    with col1:
        prev_lbl = f"₹ {prev_val:,.2f}" if prev_val is not None else "N/A"
        st.metric(f"Prev Month End ({PREV_MONTH_END_STR})", prev_lbl)
    with col2:
        today_lbl = f"₹ {today_val:,.2f}" if today_val is not None else "N/A"
        st.metric(f"Today ({_today_str})", today_lbl)
    with col3:
        if diff_val is not None:
            diff_lbl = f"{'▲' if diff_val >= 0 else '▼'} ₹ {abs(diff_val):,.2f}"
            st.metric("Movement", diff_lbl, delta_color="off")
        else:
            st.metric("Movement", "N/A")
    
    # Outstanding by company
    if st.session_state.out_today_co or st.session_state.out_prev_co:
        all_cos = sorted(set(list(st.session_state.out_prev_co.keys()) + list(st.session_state.out_today_co.keys())))
        
        rows = []
        for co in all_cos:
            p = st.session_state.out_prev_co.get(co, 0)
            t = st.session_state.out_today_co.get(co, 0)
            rows.append({
                "Company": co,
                "Prev Month End": f"₹ {p:,.2f}",
                "Today": f"₹ {t:,.2f}",
                "Movement": f"{'▲' if (t-p) >= 0 else '▼'} ₹ {abs(t-p):,.2f}"
            })
        
        summary_df = pd.DataFrame(rows)
        st.dataframe(summary_df, use_container_width=True, hide_index=True)


# ─────────────────────────────────────────────
#  MAIN ENTRY POINT
# ─────────────────────────────────────────────

def main():
    st.markdown("""
    <style>
    [data-testid="stMetricValue"] { font-size: 24px; }
    </style>
    """, unsafe_allow_html=True)
    
    # Auto-load data on first visit
    if st.session_state.df_snap is None and st.session_state.df_payment is None and not st.session_state.is_loading:
        with st.spinner("Loading initial data..."):
            run_automation()
    
    render_dashboard()
    
    # Footer
    st.divider()
    st.caption("🏢 Sangeeth MIS Workspace Controller • Powered by Streamlit")


if __name__ == "__main__":
    main()
