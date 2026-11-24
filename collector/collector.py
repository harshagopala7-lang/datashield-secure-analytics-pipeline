"""DataShield Collector (private Collector subnet, port 5000).

NOTE: Reconstructed from the project report and observed log output
(docs/screenshots/20-collector-logs.png). Review against the version
running on your Collector EC2 before relying on it.

Flow: ALB (/collect) -> Collector -> Analyzer (port 5001)
"""
import json
import os
from datetime import datetime

import requests
from flask import Flask, jsonify, request

app = Flask(__name__)

BASE_DIR = os.path.expanduser("~/collector_data")
RAW_DIR = os.path.join(BASE_DIR, "raw")
LOG_DIR = os.path.join(BASE_DIR, "logs")
LOG_FILE = os.path.join(LOG_DIR, "collector.log")
ANALYZER_URL = os.environ.get("ANALYZER_URL", "http://10.60.20.250:5001/analyze")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(LOG_DIR, exist_ok=True)


def log(message):
    line = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | {message}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "DataShield Collector"})


@app.route("/collect", methods=["POST"])
def collect():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "device_id" not in data or "value" not in data:
        log("ERROR: invalid payload (device_id and value required)")
        return jsonify({"status": "error", "message": "device_id and value are required"}), 400

    filename = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json"
    with open(os.path.join(RAW_DIR, filename), "w") as f:
        json.dump(data, f)
    log(f"RAW DATA STORED: {filename}")

    payload = dict(data, filename=filename)
    try:
        resp = requests.post(ANALYZER_URL, json=payload, timeout=15)
        log(f"FORWARDED TO ANALYZER: {filename} | status={resp.status_code}")
        return jsonify({"status": "forwarded", "analyzer_status": resp.status_code, "file": filename}), resp.status_code
    except requests.exceptions.RequestException as e:
        log(f"ANALYZER ERROR: {filename} | {e}")
        return jsonify({"status": "error", "message": "analyzer unreachable"}), 502


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
