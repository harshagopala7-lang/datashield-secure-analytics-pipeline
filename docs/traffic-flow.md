# End-to-end traffic flow

## Ingestion & processing
1. User picks a JSON file in the dashboard (`{"device_id": "...", "value": 92.5}`).
2. Browser POSTs over HTTPS to **CloudFront** → **API Gateway** (`POST /collect`).
3. API Gateway integrates with the **ALB** `/collect` rule (priority 10) → **Collector TG** (5000).
4. **Collector** validates, stores raw JSON, forwards to **Analyzer** (5001 `/analyze`); raw files are rsynced to the **Archive** every 5 min.
5. **Analyzer** processes and uploads to `s3://datashield-processed-2026/processed/<file>.json`.
6. S3 `ObjectCreated` → **Lambda** (VPC-attached) → inserts into **RDS** `security_analysis`.

## Retrieval
7. Client → ALB (default rule) → **Service** ASG (5000) → RDS (3306) → JSON/dashboard back to the client.
Endpoints: `/health`, `/security-analysis/latest`, `/dashboard-ui`.

```
User → CloudFront → API Gateway → ALB → Collector → Analyzer → S3 → Lambda → RDS
User → ALB → Service (ASG 2–6) → RDS
```
