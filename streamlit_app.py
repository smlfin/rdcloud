#!/usr/bin/env python3
"""
Sangeeth MIS Dashboard — Lightweight Version (No Playwright)

How to use:
1. Manually export MIS reports as CSV files
2. Upload CSV files to 'data/' folder in GitHub repo
3. This app displays them

OR: Manually update data by uploading new CSV files
"""

import streamlit as st
import pandas as pd
from datetime import datetime

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

DATA_FOLDER = "data/"

# ─────────────────────────────────────────────
#  LOAD DATA
# ─────────────────────────────────────────────

@st.cache_data
def load_csv(filename):
    """Load CSV file from data folder"""
    try:
        return pd.read_csv(f"{DATA_FOLDER}{filename}")
    except FileNotFoundError:
        return None
    except Exception as e:
        st.warning(f"Error loading {filename}: {e}")
        return None

# ─────────────────────────────────────────────
#  MAIN DASHBOARD
# ─────────────────────────────────────────────

def main():
    # Header
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("📊 Sangeeth MIS Dashboard")
        st.caption("Financial reporting dashboard — CSV-based version")
    
    with col2:
        if st.button("🔄 Refresh Data", use_container_width=True):
            st.cache_data.clear()
            st.rerun()
    
    st.divider()
    
    # Try to load data
    df_mis1 = load_csv("mis1.csv")
    df_mis2 = load_csv("mis2.csv")
    df_mis4 = load_csv("mis4.csv")
    
    if df_mis1 is None and df_mis2 is None and df_mis4 is None:
        st.warning("📁 No data files found!")
        st.info("""
        **How to use this dashboard:**
        
        1. Manually export MIS reports from your system as CSV files:
           - `mis1.csv` - RD Active Accounts
           - `mis2.csv` - Payment Collections
           - `mis4.csv` - Outstanding Deposits
        
        2. Create a `data/` folder in your GitHub repo
        
        3. Upload CSV files to `data/` folder
        
        4. Push to GitHub → Auto-deploys!
        
        **Or**: Use the "Upload Files" section below to add data directly.
        """)
        
        # File uploader
        st.subheader("📤 Upload CSV Files")
        uploaded_files = st.file_uploader(
            "Choose CSV files",
            type=["csv"],
            accept_multiple_files=True
        )
        
        if uploaded_files:
            st.success(f"Uploaded {len(uploaded_files)} files")
            for file in uploaded_files:
                df = pd.read_csv(file)
                st.write(f"**{file.name}** - {len(df)} rows")
                st.dataframe(df.head(10), use_container_width=True)
        
        return
    
    # MIS 1
    if df_mis1 is not None:
        st.subheader("▸ MIS 1 — RD Active Accounts & Instalment")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Accounts", f"{len(df_mis1):,}")
        with col2:
            if "Instalment" in df_mis1.columns:
                total = df_mis1["Instalment"].sum()
                st.metric("Total Instalment", f"₹ {total:,.2f}")
        
        st.dataframe(df_mis1, use_container_width=True)
    else:
        st.info("ℹ️ MIS 1 data not available - upload mis1.csv")
    
    st.divider()
    
    # MIS 2
    if df_mis2 is not None:
        st.subheader("▸ MIS 2 — Monthly Closing Report (Payment Collections)")
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Total Transactions", f"{len(df_mis2):,}")
        with col2:
            if "Principal" in df_mis2.columns:
                total = df_mis2["Principal"].sum()
                st.metric("Total Principal", f"₹ {total:,.2f}")
        
        st.dataframe(df_mis2, use_container_width=True)
    else:
        st.info("ℹ️ MIS 2 data not available - upload mis2.csv")
    
    st.divider()
    
    # MIS 3 - Calculated
    if df_mis1 is not None and df_mis2 is not None:
        st.subheader("▸ MIS 3 — Net for the Month")
        
        inst_total = df_mis1["Instalment"].sum() if "Instalment" in df_mis1.columns else 0
        amt_total = df_mis2["Amount"].sum() if "Amount" in df_mis2.columns else 0
        net_total = inst_total - amt_total
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("MIS 1 Instalment", f"₹ {inst_total:,.2f}")
        with col2:
            st.metric("MIS 2 Amount", f"₹ {amt_total:,.2f}")
        with col3:
            delta = f"{'▲' if net_total >= 0 else '▼'} ₹ {abs(net_total):,.2f}"
            st.metric("Net", delta)
    
    st.divider()
    
    # MIS 4
    if df_mis4 is not None:
        st.subheader("▸ MIS 4 — Deposit Outstanding")
        
        st.dataframe(df_mis4, use_container_width=True)
    else:
        st.info("ℹ️ MIS 4 data not available - upload mis4.csv")
    
    st.divider()
    st.caption("💾 Last updated: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


if __name__ == "__main__":
    main()
