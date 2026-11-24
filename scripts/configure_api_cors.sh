#!/bin/bash
# Enables CORS on the HTTP API for the dashboard's ALB origin only.
# Usage: ./configure_api_cors.sh <api-id> <alb-origin-url>
#   e.g. ./configure_api_cors.sh izrji7ncui http://datashield-alb-xxxx.ap-southeast-2.elb.amazonaws.com
set -euo pipefail
API_ID="${1:?api id}"; ORIGIN="${2:?alb origin}"; REGION="${AWS_REGION:-ap-southeast-2}"
aws apigatewayv2 update-api --api-id "$API_ID" --region "$REGION" \
  --cors-configuration "AllowOrigins=${ORIGIN},AllowMethods=GET,POST,OPTIONS,AllowHeaders=Content-Type"
aws apigatewayv2 get-api --api-id "$API_ID" --region "$REGION" --query CorsConfiguration
