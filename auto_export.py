#!/usr/bin/env python3
"""
Sangeeth MIS Data Exporter
Runs on your computer daily to fetch and export CSVs to GitHub

Usage:
    python auto_export.py

Schedule with:
- Windows: Task Scheduler (daily at 8 AM)
- Mac/Linux: cron job (daily at 8 AM)
"""

from playwright.sync_api import sync_playwright
from datetime import datetime, date
from calendar import monthrange
import pandas as pd
import subprocess
import os
import sys

# ─────────────────────────────────────────────
#  CONFIG
# ─────────────────────────────────────────────

BASE_URL = "http://202.21.37.156/Sangeeth/"
USERNAME = "SNL4576"
PASSWORD = "Snl@4576"

_today = datetime.today()
_today_str = _today.strftime("%d/%m/%Y")
_today_date_str = _today.strftime("%Y%m%d")
FROM_DATE_MONTH = _today.replace(day=1).strftime("%d/%m/%Y")

_d = _today.date()
if _d.month == 1:
    _prev_last = date(_d.year - 1, 12, 31)
else:
    _prev_last = date(_d.year, _d.month - 1, monthrange(_d.year, _d.month - 1)[1])
PREV_MONTH_END_STR = _prev_last.strftime("%d/%m/%Y")

# Output folder
DATA_FOLDER = "data/"
os.makedirs(DATA_FOLDER, exist_ok=True)

# ─────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────

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
        print(f"❌ Download error: {e}")
        return False

def read_xls_file(file_path):
    try:
        return pd.read_excel(file_path, engine='openpyxl')
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return None

# ─────────────────────────────────────────────
#  EXPORT FUNCTION
# ─────────────────────────────────────────────

def export_all_data():
    """Fetch all MIS data and export as CSV"""
    
    print(f"\n{'='*60}")
    print(f"  Sangeeth MIS Data Export")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}\n")
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context()
            page = context.new_page()
            
            # Login
            print("🔑 Logging in...")
            page.goto(BASE_URL, timeout=60000)
            page.fill("input[name='username']", USERNAME)
            page.fill("input[name='password']", PASSWORD)
            page.click("button[type='submit']")
            page.wait_for_load_state("networkidle")
            print("   ✅ Logged in")
            
            # MIS 1
            print("\n📋 Fetching MIS 1 (RD Active Accounts)...")
            page.goto(f"{BASE_URL}mis1", timeout=60000)
            page.wait_for_load_state("networkidle")
            fill_date(page, "From Date", FROM_DATE_MONTH)
            fill_date(page, "To Date", _today_str)
            
            mis1_file = f"/tmp/mis1_{_today_date_str}.xls"
            if generate_and_download(context, page, mis1_file):
                df = read_xls_file(mis1_file)
                if df is not None:
                    output_file = f"{DATA_FOLDER}mis1.csv"
                    df.to_csv(output_file, index=False)
                    print(f"   ✅ Exported: {output_file} ({len(df)} rows)")
                else:
                    print(f"   ⚠️  Failed to read MIS 1 file")
            
            # MIS 2
            print("\n💳 Fetching MIS 2 (Payment Collections)...")
            page.goto(f"{BASE_URL}mis2", timeout=60000)
            page.wait_for_load_state("networkidle")
            fill_date(page, "From Date", FROM_DATE_MONTH)
            fill_date(page, "To Date", _today_str)
            
            mis2_file = f"/tmp/mis2_{_today_date_str}.xls"
            if generate_and_download(context, page, mis2_file):
                df = read_xls_file(mis2_file)
                if df is not None:
                    output_file = f"{DATA_FOLDER}mis2.csv"
                    df.to_csv(output_file, index=False)
                    print(f"   ✅ Exported: {output_file} ({len(df)} rows)")
                else:
                    print(f"   ⚠️  Failed to read MIS 2 file")
            
            # MIS 4
            print("\n📈 Fetching MIS 4 (Deposit Outstanding)...")
            page.goto(f"{BASE_URL}mis4", timeout=60000)
            page.wait_for_load_state("networkidle")
            fill_ason_date(page, _today_str)
            
            mis4_file = f"/tmp/mis4_{_today_date_str}.xls"
            if generate_and_download(context, page, mis4_file):
                df = read_xls_file(mis4_file)
                if df is not None:
                    output_file = f"{DATA_FOLDER}mis4.csv"
                    df.to_csv(output_file, index=False)
                    print(f"   ✅ Exported: {output_file} ({len(df)} rows)")
                else:
                    print(f"   ⚠️  Failed to read MIS 4 file")
            
            browser.close()
        
        # Git commit & push
        print("\n📤 Pushing to GitHub...")
        os.system("git add data/")
        os.system(f'git commit -m "Auto-export MIS data {_today_str}"')
        os.system("git push origin main")
        print("   ✅ Pushed to GitHub")
        
        print(f"\n{'='*60}")
        print(f"✅ Export completed successfully!")
        print(f"   CSVs available in: {DATA_FOLDER}")
        print(f"   Streamlit app auto-reloads on GitHub")
        print(f"{'='*60}\n")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Export failed: {e}")
        print(f"{'='*60}\n")
        return False

# ─────────────────────────────────────────────
#  ENTRY POINT
# ─────────────────────────────────────────────

if __name__ == "__main__":
    success = export_all_data()
    sys.exit(0 if success else 1)
