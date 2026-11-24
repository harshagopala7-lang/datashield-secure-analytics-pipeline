# Problems encountered & fixes

| Problem | Fix |
|---|---|
| SSH timeout (My IP option unavailable) | Corrected the inbound SSH rule; access private hosts via Bastion |
| Private dashboard timeout | Checked route tables, SGs, ALB target health, listener path |
| 400/500 from PowerShell curl | Send JSON from a file (`--data @file`), correct Content-Type |
| Analyzer S3 upload failure | Create `boto3` client inside the upload function (instance role at runtime) |
| Browser "Failed to fetch" | Enable CORS on the HTTP API for the ALB origin |
| ASG launched old config | Set LT v3 as default and run an instance refresh / replace instances |
| Archive volume after reboot | Unlock LUKS2 manually; passphrase never stored |
