# dashboard.py
import streamlit as st
import json
import os
from datetime import datetime

LOG_PATH = "logs/log.jsonl"

# Load log entries from JSONL
@st.cache_data
def load_logs():
    if not os.path.exists(LOG_PATH):
        return []
    with open(LOG_PATH, "r") as f:
        return [json.loads(line) for line in f if line.strip()]

# Format timestamp for display
def format_ts(ts):
    try:
        return datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ts

# Streamlit UI
st.set_page_config(page_title="AIBBR Dashboard", layout="wide")
st.title("AI Incident Black Box Recorder Dashboard")

logs = load_logs()

if not logs:
    st.warning("No logs found yet.")
    st.stop()

# Sidebar filters
model_names = sorted(set(log["model_name"] for log in logs))
selected_model = st.sidebar.selectbox("Model", ["All"] + model_names)
tags = sorted(set(tag for log in logs for tag in log["tags"]))
selected_tag = st.sidebar.selectbox("Tag", ["All"] + tags)

# Filtered logs
filtered = logs
if selected_model != "All":
    filtered = [log for log in filtered if log["model_name"] == selected_model]
if selected_tag != "All":
    filtered = [log for log in filtered if selected_tag in log["tags"]]

st.metric("Total Logs", len(filtered))

# Table view
for log in filtered[::-1]:
    with st.expander(f" {log['model_name']} — {format_ts(log['timestamp'])}"):
        st.markdown(f"**Input:** `{log['input']}`")
        st.markdown(f"**Output:** `{log['output']}`")
        st.markdown(f"**Success:** {log['success']}")
        st.markdown(f"**Latency:** `{log['latency_sec']}s`")
        st.markdown(f"**Tags:** `{', '.join(log['tags'])}`")
        st.caption(f"Log ID: `{log['id']}`")
