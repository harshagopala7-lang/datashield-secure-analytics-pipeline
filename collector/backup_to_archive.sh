#!/bin/bash
# Copies raw Collector data to the isolated, LUKS2-encrypted Archive EC2.
# Scheduled every 5 minutes (see crontab.example). Requires SSH key access
# from Collector to Archive (both inside the VPC; Archive has no internet route).
set -euo pipefail
ARCHIVE_HOST="${ARCHIVE_HOST:?set ARCHIVE_HOST to the Archive private IP}"
SRC="$HOME/collector_data/raw/"
DEST="/archive/raw/"
rsync -az -e "ssh -o StrictHostKeyChecking=accept-new" "$SRC" "ec2-user@${ARCHIVE_HOST}:${DEST}"
echo "$(date '+%F %T') | BACKUP OK -> ${ARCHIVE_HOST}:${DEST}" >> "$HOME/collector_data/logs/backup.log"
