# Deployment guide (high level)

Console/CLI steps in build order. Replace IDs/endpoints with your own.

1. **VPC & subnets** – create `10.60.0.0/16` and the subnets in `infrastructure/network.md`.
2. **IGW + NAT** – attach IGW; NAT Gateway in Public-Edge-Subnet-A.
3. **Route tables** – Public-RT, Private-NAT-RT, DB-RT (local), Archive-RT (local); associate as tabled.
4. **Security groups** – create per the matrix; reference SGs by ID, not CIDR.
5. **Bastion** – public EC2 in Public-Edge-Subnet-A.
6. **RDS MySQL** – private, public access off, subnet group = DB-A/B, SG `DB-SG`; run `database/schema.sql`.
7. **S3** – `datashield-processed-2026` with versioning, block public access, SSE-S3, lifecycle (noncurrent versions deleted after 30 days).
8. **IAM** – Analyzer role (`s3:PutObject` on `processed/*`); Lambda role (VPC access + `s3:GetObject`).
9. **Archive EC2** – isolated subnet; `archive/setup_luks_archive.sh`.
10. **Collector EC2** – install `collector/`, enable `datashield-collector.service`, add cron from `collector/crontab.example`.
11. **Analyzer EC2** – install `analyzer/`, enable `datashield-analyzer.service`.
12. **Service EC2** – install `service/`, create `/etc/datashield/service.env` from `.env.example`, enable `datashield-api.service`.
13. **Lambda** – `lambda/build.sh`, deploy, set env vars, VPC config, S3 trigger on `processed/`.
14. **ALB** – listener :80 default → Service TG (5000, health `/health`); rule priority 10 `/collect*` → Collector TG.
15. **API Gateway (HTTP API)** – `POST /collect` → ALB `/collect`; run `scripts/configure_api_cors.sh`.
16. **CloudFront** – origin = API Gateway, redirect HTTP→HTTPS, allow GET/HEAD/OPTIONS/PUT/POST/PATCH/DELETE, caching disabled.
17. **Service AMI + Launch Template + ASG** – bake `DataShield-Service-Final-AMI`, LT v3 default, ASG min 2 / desired 2 / max 6, CPU target-tracking policy, attach to Service TG.
18. **Validate** – `scripts/test_upload.sh`, then check dashboard `/dashboard-ui` and CloudWatch logs.

Service unit setup example:

```bash
sudo mkdir -p /etc/datashield && sudo cp .env /etc/datashield/service.env && sudo chmod 600 /etc/datashield/service.env
sudo cp service/datashield-api.service /etc/systemd/system/
sudo systemctl daemon-reload && sudo systemctl enable --now datashield-api
```
