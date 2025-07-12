# This file handles logging to a JSON Lines (.jsonl) file, where each line is a JSON object representing a log entry.

import json
import os

LOG_PATH = "logs/log.jsonl"
os.makedirs("logs", exist_ok=True)

def log_entry(data):
    with open(LOG_PATH, "a") as f:
        f.write(json.dumps(data) + "\n")

def tag_last_entry(tag):
    with open(LOG_PATH, "r") as f:
        lines = f.readlines()

    if not lines:
        return

    last = json.loads(lines[-1])
    last["tags"].append(tag)
    lines[-1] = json.dumps(last) + "\n"

    with open(LOG_PATH, "w") as f:
        f.writelines(lines)
