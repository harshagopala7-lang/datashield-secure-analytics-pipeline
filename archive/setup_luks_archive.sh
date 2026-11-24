#!/bin/bash
# Sets up the encrypted /archive volume on the isolated Archive EC2.
# Run interactively as root/sudo. The passphrase is typed at the prompt and
# is NEVER stored in this repo, logs, or scripts.
#
# Usage: sudo ./setup_luks_archive.sh /dev/nvme1n1
set -euo pipefail
DEV="${1:?usage: $0 <device, e.g. /dev/nvme1n1>}"
NAME="archive_crypt"

read -r -p "This will ERASE ${DEV}. Type YES to continue: " ok
[ "$ok" = "YES" ] || { echo "aborted"; exit 1; }

cryptsetup luksFormat --type luks2 "$DEV"        # prompts for passphrase
cryptsetup open "$DEV" "$NAME"                   # prompts for passphrase
mkfs.xfs "/dev/mapper/${NAME}"
mkdir -p /archive
mount "/dev/mapper/${NAME}" /archive
mkdir -p /archive/raw /archive/logs /archive/backups
chown -R ec2-user:ec2-user /archive

echo "LUKS UUID: $(cryptsetup luksUUID "$DEV")"
cryptsetup luksDump "$DEV" | head -25
df -h /archive
