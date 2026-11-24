"""DataShield Service tier (Flask backend + dashboard).

Runs on the private Service EC2 instances (Auto Scaling Group, port 5000)
behind the Application Load Balancer. Reads processed results from the
private RDS MySQL database.

Configuration is read from environment variables (see .env.example) so that
no credentials are stored in source control.
"""
import os

import pymysql
from flask import Flask, jsonify, render_template

app = Flask(__name__)

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_NAME = os.environ.get("DB_NAME", "datashield")


def get_connection():
    return pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5,
        cursorclass=pymysql.cursors.DictCursor,
    )


@app.route("/")
def home():
    return "DataShield Service API is running!"


@app.route("/health")
def health():
    """ALB target-group health check; also verifies RDS connectivity."""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        connection.close()
        return jsonify({
            "status": "healthy",
            "service": "DataShield Service",
            "database": "RDS MySQL",
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/security-analysis/latest", methods=["GET"])
def get_latest_analysis():
    """Return the 10 most recent processed records for the dashboard."""
    try:
        connection = get_connection()
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT id, analysis_time, device_id, input_value,
                       processed_value, status, result
                FROM security_analysis
                ORDER BY id DESC
                LIMIT 10
                """
            )
            records = cursor.fetchall()
        connection.close()
        return jsonify({"status": "success", "count": len(records), "data": records})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


@app.route("/dashboard-ui")
def dashboard_ui():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
