#!/bin/bash
# Expect HTTP 204 with Access-Control-Allow-* headers.
# Usage: ./test_cors_preflight.sh https://<cloudfront-domain>/collect <alb-origin>
set -euo pipefail
curl -i -X OPTIONS "${1:?cloudfront /collect url}" \
  -H "Origin: ${2:?origin}" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: Content-Type"
