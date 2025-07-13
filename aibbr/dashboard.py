# dashboard.py (SQLite with search & date filters)
import streamlit as st
import sqlite3
import os
from datetime import datetime

DB_PATH = "logs/logs.db"

st.set_page_config(page_title="AIBBR Dashboard", layout="wide")
st.title("AI Incident Black Box Recorder Dashboard")

if not os.path.exists(DB_PATH):
    st.warning("No SQLite database found at logs/logs.db")
    st.stop()

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Load logs from DB
cursor.execute("SELECT * FROM logs")
rows = cursor.fetchall()
columns = [desc[0] for desc in cursor.description]
logs = [dict(zip(columns, row)) for row in rows]

# Sidebar filters
model_names = sorted(set(log["model_name"] for log in logs))
selected_model = st.sidebar.selectbox("Model", ["All"] + model_names)

# Tags
tag_set = set()
for log in logs:
    tag_set.update(tag.strip() for tag in log["tags"].split(",") if tag.strip())
tags = sorted(tag_set)
selected_tag = st.sidebar.selectbox("Tag", ["All"] + tags)

# Search
search_input = st.sidebar.text_input("Search input/output")

# Date range filter
timestamps = [datetime.fromisoformat(log["timestamp"]) for log in logs]
if timestamps:
    min_date = min(timestamps).date()
    max_date = max(timestamps).date()
    start_date, end_date = st.sidebar.date_input("Filter by date range", [min_date, max_date])
else:
    start_date, end_date = None, None

# Filtered logs
filtered = logs
if selected_model != "All":
    filtered = [log for log in filtered if log["model_name"] == selected_model]
if selected_tag != "All":
    filtered = [log for log in filtered if selected_tag in log["tags"].split(",")]
if search_input:
    filtered = [log for log in filtered if search_input.lower() in log["input"].lower() or search_input.lower() in log["output"].lower()]
if start_date and end_date:
    filtered = [log for log in filtered if start_date <= datetime.fromisoformat(log["timestamp"]).date() <= end_date]

st.metric("Total Logs", len(filtered))

def format_ts(ts):
    try:
        return datetime.fromisoformat(ts).strftime("%Y-%m-%d %H:%M:%S")
    except:
        return ts

# Table view
for log in filtered[::-1]:
    with st.expander(f"{log['model_name']} — {format_ts(log['timestamp'])}"):
        st.markdown(f"**Input:** `{log['input']}`")
        st.markdown(f"**Output:** `{log['output']}`")
        st.markdown(f"**Success:** {log['success']}")
        st.markdown(f"**Latency:** `{log['latency_sec']}s`")
        st.markdown(f"**Tags:** `{log['tags']}`")
        st.caption(f"Log ID: `{log['id']}`")
