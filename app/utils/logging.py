import json
import os
import time

LOG_FILE = "results/audit_log.json"

def write_log(entry: dict):
    os.makedirs("results", exist_ok=True)
    logs = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except:
            logs = []
            
    entry["timestamp"] = time.time()
    logs.append(entry)
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4)