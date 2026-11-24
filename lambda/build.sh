#!/bin/bash
# Builds DataShield-Lambda.zip (Linux/macOS/WSL/CloudShell).
# PyMySQL is pure Python, so a plain pip install --target works.
set -euo pipefail
cd "$(dirname "$0")"
rm -rf package DataShield-Lambda.zip
mkdir package
pip install --target package -r requirements.txt
cp lambda_function.py package/
(cd package && zip -qr ../DataShield-Lambda.zip .)
echo "Built $(pwd)/DataShield-Lambda.zip"
