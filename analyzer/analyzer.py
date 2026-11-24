"""Cron-driven security metrics analyzer (early prototype stage).

Collects real CPU usage plus simulated security indicators, applies simple
rules, and POSTs the result to the Service tier. Scheduled every 5 minutes:

  */5 * * * * /usr/bin/python3 /home/ec2-user/analyzer.py >> /home/ec2-user/analyzer.log 2>&1

NOTE: the Service tier in this repo (service/app.py) is the final version and
no longer exposes POST /security-analysis. Keep this file as a reference for
the rule-based threat logic, or re-add that route if you want to run it.
"""
import os
import random
from datetime import datetime

import psutil
import requests

SERVICE_URL = os.environ.get("SERVICE_URL", "http://10.60.30.37:5000/security-analysis")

cpu_usage = round(psutil.cpu_percent(interval=1), 2)

# Simulated security activity for demonstration purposes
failed_login_attempts = random.randint(0, 10)
suspicious_ip = random.choice([True, False])

alerts = []
if failed_login_attempts > 5:
    alerts.append("High number of failed login attempts detected")
if cpu_usage > 85:
    alerts.append("High CPU usage detected")
if suspicious_ip:
    alerts.append("Suspicious IP activity detected")

if alerts:
    status = "THREAT DETECTED"
    result = " | ".join(alerts)
else:
    status = "SAFE"
    result = "No security threats detected"

data = {
    "source_instance": "DataShield-Analyzer-EC2",
    "analysis_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "status": status,
    "failed_login_attempts": failed_login_attempts,
    "cpu_usage": cpu_usage,
    "suspicious_ip": suspicious_ip,
    "result": result,
}

print("\n--- DataShield Security Analysis ---")
for k in ("failed_login_attempts", "cpu_usage", "suspicious_ip", "status", "result"):
    print(f"{k}: {data[k]}")

try:
    response = requests.post(SERVICE_URL, json=data, timeout=10)
    print("\nHTTP Status:", response.status_code)
    print("Response:", response.json())
except requests.exceptions.RequestException as e:
    print("Failed to send analysis result:", e)
