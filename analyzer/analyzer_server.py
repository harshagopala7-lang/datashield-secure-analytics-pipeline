"""DataShield Analyzer (private Analyzer subnet, port 5001).

NOTE: Reconstructed from the project report, the S3-client fix documented in
the code export, and observed logs (docs/screenshots/21-analyzer-s3-logs.png).
Review against the version running on your Analyzer EC2.

Receives JSON from the Collector, validates/processes it, and uploads the
result to s3://<bucket>/processed/<filename>. The S3 ObjectCreated event then
triggers the VPC-attached Lambda which inserts into RDS.
Uses the EC2 instance IAM role - no static credentials.
"""
import json
import os
from datetime import datetime, timezone

import boto3
from flask import Flask, jsonify, request

app = Flask(__name__)

BUCKET = os.environ.get("S3_BUCKET", "datashield-processed-2026")
REGION = os.environ.get("AWS_REGION", "ap-southeast-2")
LOG_DIR = os.path.expanduser("~/analyzer_data/logs")
LOG_FILE = os.path.join(LOG_DIR, "analyzer.log")
os.makedirs(LOG_DIR, exist_ok=True)


def get_s3_client():
    # Created at call time so the instance-role credentials are resolved at
    # runtime (fixes the earlier module-level client initialisation issue).
    return boto3.client("s3", region_name=REGION)


def log(message):
    line = f"{datetime.now().isoformat()} - {message}"
    print(line, flush=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "service": "DataShield Analyzer"})


@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.get_json(silent=True)
    if not isinstance(data, dict) or "device_id" not in data or "value" not in data:
        return jsonify({"status": "error", "message": "device_id and value are required"}), 400
    try:
        value = round(float(data["value"]), 2)
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "value must be numeric"}), 400

    filename = data.get("filename") or datetime.now().strftime("%Y%m%d_%H%M%S_%f") + ".json"
    processed = {
        "device_id": str(data["device_id"]),
        "input_value": value,
        "processed_value": value,
        "status": "processed",
        "processed_at": datetime.now(timezone.utc).isoformat(),
    }

    try:
        s3 = get_s3_client()
        s3_key = f"processed/{filename}"
        s3.put_object(Bucket=BUCKET, Key=s3_key, Body=json.dumps(processed),
                      ContentType="application/json")
        log(f"S3 UPLOAD SUCCESS: s3://{BUCKET}/{s3_key}")
        return jsonify({"status": "success", "s3_key": s3_key}), 200
    except Exception as e:
        log(f"S3 UPLOAD ERROR: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
