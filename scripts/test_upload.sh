#!/bin/bash
# Sends a sample JSON payload through the full pipeline.
# Usage: ./test_upload.sh https://<cloudfront-domain>/collect [device_id] [value]
set -euo pipefail
URL="${1:?cloudfront /collect url}"
printf '{"device_id":"%s","value":%s}' "${2:-DASHBOARD-UPLOAD-001}" "${3:-92.50}" > /tmp/ds_payload.json
curl -i -X POST "$URL" -H "Content-Type: application/json" --data @/tmp/ds_payload.json
