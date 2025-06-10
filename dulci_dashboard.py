import streamlit as st
import pandas as pd
import json
import os
import time

st.set_page_config(
    page_title="DULCi Live Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("📡 DULCi Live Trading Dashboard")

# --- SYSTEM MODE ---
mode_placeholder = st.empty()

# --- STATUS COLUMNS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔍 Coin Hunter")
    if os.path.exists("runtime/coinhunter_status.json"):
        with open("runtime/coinhunter_status.json") as f:
            data = json.load(f)
            st.markdown(f"**Hot Pair:** `{data.get('pair', '-')}`")
            st.markdown(f"**Confidence:** `{data.get('confidence', '-')}`")
            st.markdown(f"**Signal Reason:** `{data.get('reason', '-')}`")
    else:
        st.warning("No data yet.")

with col2:
    st.subheader("📈 Price Predictor")
    if os.path.exists("runtime/price_prediction.json"):
        with open("runtime/price_prediction.json") as f:
            data = json.load(f)
            st.markdown(f"**Next Move:** `{data.get('direction', '-')}`")
            st.markdown(f"**Target Price:** `{data.get('price', '-')}`")
            st.markdown(f"**Model Accuracy:** `{data.get('accuracy', '-')}`")
    else:
        st.warning("No prediction data.")

with col3:
    st.subheader("🤖 Execution Engine")
    if os.path.exists("runtime/execution_status.json"):
        with open("runtime/execution_status.json") as f:
            data = json.load(f)
            st.markdown(f"**Running Mode:** `{data.get('mode', '-')}`")
            st.markdown(f"**Trade Status:** `{data.get('status', '-')}`")
            st.markdown(f"**Last Action:** `{data.get('last_action', '-')}`")
    else:
        st.warning("No executor updates.")

# --- PORTFOLIO OVERVIEW ---
st.subheader("📊 Portfolio Tracker")
if os.path.exists("runtime/portfolio.csv"):
    df = pd.read_csv("runtime/portfolio.csv")
    st.dataframe(df, use_container_width=True)
else:
    st.info("Portfolio data will appear here.")

# --- LOG READER ---
st.subheader("📁 Live Logs")
log_option = st.selectbox("Select log type", ["trading", "coinhunter", "predictor", "errors"])
log_path = f"logs/{log_option}.log"

if os.path.exists(log_path):
    with open(log_path, "r") as f:
        logs = f.readlines()[-100:]
        st.text("".join(logs))
else:
    st.info("No logs available for this section.")

# --- LIVE REFRESH ---
st.markdown("---")
st.caption("Refreshing every 5 seconds...")
st_autorefresh = st.experimental_rerun

# Add delay manually to allow this run to complete
# After deployment with `streamlit run`, use Streamlit's built-in auto-refresh
# or tmux/systemd for runtime persistence
