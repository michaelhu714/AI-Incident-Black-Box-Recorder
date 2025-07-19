# logger.py (SQLite version)
import sqlite3
import os
from utils import get_timestamp, generate_id
import time 

DB_PATH = "logs/logs.db"
os.makedirs("logs", exist_ok=True)

# Connect and initialize table
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id TEXT PRIMARY KEY,
    timestamp TEXT,
    model_name TEXT,
    input TEXT,
    output TEXT,
    success BOOLEAN,
    latency_sec REAL,
    tags TEXT
)
""")
conn.commit()

def log_entry(data):
    cursor.execute("""
        INSERT INTO logs (id, timestamp, model_name, input, output, success, latency_sec, tags)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["id"],
        data["timestamp"],
        data["model_name"],
        data["input"],
        data["output"],
        data["success"],
        data["latency_sec"],
        ",".join(data["tags"])
    ))
    conn.commit()

def tag_last_entry(tag):
    cursor.execute("SELECT id, tags FROM logs ORDER BY timestamp DESC LIMIT 1")
    row = cursor.fetchone()
    if not row:
        return
    log_id, tags_str = row
    tags = tags_str.split(",") if tags_str else []
    tags.append(tag)
    cursor.execute("UPDATE logs SET tags = ? WHERE id = ?", (",".join(tags), log_id))
    conn.commit()


def log_interaction(input_text, output_text, model_name, status="success", tags=None):
    if tags is None:
        tags = []
    latency = 0.0  # Default latency

    # Measure latency if output_text is not an error
    if status == "success":
        start_time = time.time()
        # Simulate time for latency calculation (replace if you measure elsewhere)
        end_time = time.time()
        latency = round(end_time - start_time, 4)

    log_entry({
        "id": generate_id(),
        "timestamp": get_timestamp(),
        "model_name": model_name,
        "input": input_text,
        "output": output_text,
        "success": status == "success",
        "latency_sec": latency,
        "tags": tags,
    })
