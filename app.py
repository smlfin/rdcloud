import os
import streamlit as st

# CRITICAL STEP FOR THE WEB SERVER: Install the headless browser automatically
if not os.path.exists("/home/appuser/.cache/ms-playwright"):
    os.system("playwright install chromium")

from playwright.sync_api import sync_playwright
from datetime import datetime, date
from calendar import monthrange
import pandas as pd
import re

# ─────────────────────────────────────────────
#  CONFIGURATION & HELPERS
# ─────────────────────────────────────────────
BASE_URL = "http://202.21.37.156/Sangeeth/"
USERNAME = "SNL4576"
PASSWORD = "Snl@4576"

_today = datetime.today()
_today_str = _today.strftime("%d/%m/%Y")
_today_date_str = _today.strftime("%Y%m%d")
FROM_DATE_MONTH = _today.replace(day=1).strftime("%d/%m/%Y")
FROM_DATE_DETAILS = "01/01/2020"

_d = _today.date()
if _d.month == 1:
    _prev_last = date(_d.year - 1, 12, 31)
else:
    _prev_last = date(_d.year, _d.month - 1, monthrange(_d.year, _d.month - 1)[1])
PREV_MONTH_END_STR = _prev_last.strftime("%d/%m/%Y")

def normalise_company(raw):
    s = str(raw).strip()
    if not s or s.lower() == "nan": return "Unknown"
    if "VFL" in s.upper(): return "VFL"
    if "SML" in s.upper(): return "SML"
    return "SNL"

def split_staff_parts(name):
    if pd.isna(name) or str(name).strip() == "": return "", "", ""
    parts = [p.strip() for p in str(name).split("-")]
    return (
        parts[0] if len(parts) > 0 else "",
        parts[1] if len(parts) > 1 else "",
        parts[2] if len(parts) > 2 else "",
    )

def fill_date(page, label_text, date_value):
    try:
        input_id = page.locator(f"label:has-text('{label_text}')").first.get_attribute("for")
        field = page.locator(f"#{input_id}") if input_id else page.locator(f"label:has-text('{label_text}')").locator("..").locator("input").first
        field.evaluate("(el, val) => { el.value = val; el.dispatchEvent(new Event('change', {bubbles:true})); }", date_value)
        field.click(click_count=3)
        field.type(date_value)
    except: pass

def fill_ason_date(page, date_value):
    try:
        page.evaluate("(val) => { const ins = Array.from(document.querySelectorAll('input[type=text]')); if(ins[0]){ ins[0].value = val; ins[0].dispatchEvent(new Event('change', {bubbles:true})); } }", date_value)
    except: pass

def select_dropdown(page, label_text, value):
    try:
        input_id = page.locator(f"label:has-text('{label_text}')").first.get_attribute("for")
        if input_id: page.select_option(f"#{input_id}", label=value)
        else: page.locator(f"label:has-text('{label_text}')").locator("xpath=..").locator("select").first.select_option(label=value)
    except: pass

def locate_export_select(report_page):
    for p in [report_page] + report_page.frames:
        try:
            for sel in p.locator("select").all():
                if any("CSV" in o or "Excel" in o for o in sel.evaluate("el => Array.from(el.options).map(o => o.text)")):
                    return sel
        except: pass
    return None

def generate_and_download(context, page, temp_path, export_format="Excel 97-2003"):
    try:
        with context.expect_page(timeout=60000) as npi:
            page.click("button:has-text('Generate'), input[value='Generate'], button:has-text('View Report')", timeout=15000)
        rp = npi.value
        rp.wait_for_load_state("networkidle", timeout=60000)
        export_sel = locate_export_select(rp)
        if not export_sel: { rp.close(); return False }
        export_sel.select_option(label=export_format)
        with rp.expect_download(timeout=90000) as dl_info:
            rp.locator("a[id*='Export'], input[id*='Export'], button[id*='Export']").first.click(timeout=10000, no_wait_after=True)
        dl_info.value.save_as(temp_path)
        rp.close()
        return True
    except: return False

def read_xls_data_rows(filepath, repo_name):
    try: df = pd.read_excel(filepath, engine="xlrd", header=None, dtype=str)
    except: return None
    headers = ["Sl_No", "Col_Blank_1", "Date", "Deposit_No", "Share_Name", "Principal", "Interest", "Col_Blank_2", "TDS", "Total_Amount", "Int_Accrued", "PAN_No", "TDS_Type", "Pmt_Mode"] if repo_name == "NCDPayment" else ["Sl_No", "Share_Name", "Address", "Col_Blank_1", "Pan_No", "Dep_No", "Date", "Amount", "Period", "Scheme", "Col_Blank_2", "Int_Pct", "Agent", "TDS"]
    df.columns = headers[:len(df.columns)]
    df_data = df[df["Sl_No"].apply(lambda v: isinstance(v, str) and v.strip().split(".")[0].isdigit())].copy().reset_index(drop=True)
    return df_data.drop(columns=[c for c in df_data.columns if "Blank" in c], errors="ignore")

# ─────────────────────────────────────────────
#  WEB UI STRUCTURE
# ─────────────────────────────────────────────
st.set_page_config(page_title="Sangeeth MIS Dashboard", layout="wide")
st.title("📊 Sangeeth MIS Workspace Controller")
st.write("Click the button below to trigger the live background data compilation pipeline.")

if st.button("🚀 Run MIS Automation Pipeline", type="primary"):
    status_box = st.empty()
    
    with sync_playwright() as p:
        status_box.info("Authenticating with Sangeeth portal...")
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        try:
            page.goto(BASE_URL, timeout=45000)
            page.fill("input[type='text']", USERNAME)
            page.fill("input[type='password']", PASSWORD)
            page.click("input[type='submit'], button[type='submit']")
            page.wait_for_load_state("networkidle")
            
            # ── MIS 1 ──
            status_box.info("Pipeline processing: Pulling MIS 1 (Active RD Accounts)...")
            page.goto(f"{BASE_URL}Reports/ReportOptions?repo_name=NCDDetails")
            fill_date(page, "From Date", FROM_DATE_MONTH)
            fill_date(page, "To Date", _today_str)
            select_dropdown(page, "Branch", "All Branch")
            select_dropdown(page, "Staff Members", "All")
            select_dropdown(page, "Master", "RD")
            select_dropdown(page, "Scheme", "All")
            
            temp1 = f"temp_m1.csv"
            with context.expect_page(timeout=60000) as npi:
                page.click("button:has-text('Generate')")
            rp = npi.value
            sel = locate_export_select(rp)
            if sel:
                sel.select_option(label="CSV (comma delimited)")
                with rp.expect_download() as dl:
                    rp.click("a[id*='Export']")
                dl.value.save_as(temp1)
            rp.close()
            
            df_snap = pd.read_csv(temp1, header=None, dtype=str)
            df_snap.columns = ["Branch_Total", "Branch", "Branch_Amount", "Product", "Amount", "Sl_No", "Account_No", "Date", "Instalment", "Scheme", "Address", "PAN", "Customer_Name", "Duration", "Rate", "Staff_Name", "Col17", "Col18", "Mobile"][:len(df_snap.columns)]
            df_snap["Instalment"] = pd.to_numeric(df_snap["Instalment"].str.replace(",", "").str.replace("₹", ""), errors="coerce").fillna(0)
            if "Staff_Name" in df_snap.columns:
                df_snap["Company"] = df_snap["Staff_Name"].apply(lambda x: normalise_company(split_staff_parts(x)[1]))
            if os.path.exists(temp1): os.remove(temp1)
            
            # ── MIS 2 ──
            status_box.info("Pipeline processing: Pulling MIS 2 (Monthly Closing Collections)...")
            page.goto(f"{BASE_URL}Reports/ReportOptions?repo_name=NCDPayment")
            fill_date(page, "From Date", FROM_DATE_MONTH)
            fill_date(page, "To Date", _today_str)
            select_dropdown(page, "Branch", "All Branch")
            select_dropdown(page, "MasterName", "RD")
            
            temp2 = "temp_m2.xls"
            df_payment = None
            if generate_and_download(context, page, temp2):
                df_payment = read_xls_data_rows(temp2, "NCDPayment")
            if os.path.exists(temp2): os.remove(temp2)
            
            if df_payment is not None:
                df_payment["Principal"] = pd.to_numeric(df_payment["Principal"].str.replace(",", ""), errors="coerce").fillna(0)
                df_payment["Amount"] = pd.to_numeric(df_payment["Total_Amount"].str.replace(",", ""), errors="coerce").fillna(0)
                df_payment["Company"] = "SNL"  # Default fallback
                
            # ── DISPLAY RESULTS ──
            status_box.success("All MIS components compiled successfully!")
            
            # Layout Columns
            m1, m2, m3 = st.columns(3)
            tot_inst = df_snap["Instalment"].sum()
            tot_pay = df_payment["Principal"].sum() if df_payment is not None else 0
            
            m1.metric("MIS 1 Total Instalments", f"₹ {tot_inst:,.2f}")
            m2.metric("MIS 2 Total Principal", f"₹ {tot_pay:,.2f}")
            m3.metric("MIS 3 Net for Month", f"₹ {(tot_inst - tot_pay):,.2f}")
            
            st.subheader("MIS 1 Breakdown Table")
            st.dataframe(df_snap[["Account_No", "Customer_Name", "Instalment", "Company"]], use_container_width=True)
            
        except Exception as error:
            status_box.error(f"Automation Halted: {error}")
        finally:
            browser.close()