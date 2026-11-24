# Archive tier (isolated, encrypted)

- Subnet `Isolated-Archive-Subnet` (10.60.50.0/24), route table `DataShield-Archive-RT` with **local route only** (no IGW/NAT).
- Second EBS volume encrypted with **LUKS2** and formatted **XFS**, mounted at `/archive`.
- Receives raw Collector backups every 5 minutes (`collector/backup_to_archive.sh`).
- The LUKS passphrase is **not** stored anywhere in this repo. After a reboot the volume must be unlocked manually:

```bash
sudo cryptsetup open /dev/nvme1n1 archive_crypt
sudo mount /dev/mapper/archive_crypt /archive
```

Isolation proof: `docs/screenshots/26-archive-internet-blocked.png` (curl to aws.amazon.com / google.com times out).
