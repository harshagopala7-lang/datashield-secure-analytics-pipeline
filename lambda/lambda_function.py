import json
import os
import urllib.parse

import boto3
import pymysql


s3 = boto3.client("s3")


DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ.get("DB_PORT", "3306"))
DB_NAME = os.environ["DB_NAME"]
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]


def lambda_handler(event, context):

    print("Received event:")
    print(json.dumps(event))

    # Get S3 bucket and object information
    record = event["Records"][0]

    bucket = record["s3"]["bucket"]["name"]
    key = urllib.parse.unquote_plus(
        record["s3"]["object"]["key"]
    )

    print(f"Reading S3 object: s3://{bucket}/{key}")

    # Read JSON from S3
    response = s3.get_object(
        Bucket=bucket,
        Key=key
    )

    body = response["Body"].read().decode("utf-8")
    data = json.loads(body)

    print("S3 data:")
    print(json.dumps(data))

    # Extract DataShield fields
    device_id = data.get("device_id", "UNKNOWN")

    input_value = data.get(
        "input_value",
        data.get("value")
    )

    processed_value = data.get(
        "processed_value",
        data.get("value")
    )

    status = data.get(
        "status",
        "PROCESSED"
    )

    result = data.get(
        "result",
        "Processed by DataShield Analyzer"
    )

    # Connect to private RDS
    connection = pymysql.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        connect_timeout=5
    )

    try:
        with connection.cursor() as cursor:

            sql = """
                INSERT INTO security_analysis
                (
                    device_id,
                    input_value,
                    processed_value,
                    status,
                    result
                )
                VALUES
                (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
            """

            cursor.execute(
                sql,
                (
                    device_id,
                    input_value,
                    processed_value,
                    status,
                    result
                )
            )

        connection.commit()

        print(
            f"Successfully inserted analysis for device: {device_id}"
        )

        return {
            "statusCode": 200,
            "body": json.dumps({
                "status": "success",
                "message": "S3 object processed and inserted into RDS",
                "device_id": device_id
            })
        }

    finally:
        connection.close()