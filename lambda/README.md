# DataShield-S3-to-RDS (Lambda)

| Setting | Value |
|---|---|
| Runtime | Python 3.12 |
| Handler | `lambda_function.lambda_handler` |
| VPC | DataShield-VPC, subnets Private-Service-Subnet (A) & -B, SG `DataShield-Lambda-SG` |
| Trigger | S3 `ObjectCreated`, prefix `processed/`, bucket `datashield-processed-2026` |
| Env vars | `DB_HOST`, `DB_PORT` (3306), `DB_NAME`, `DB_USER`, `DB_PASSWORD` |
| IAM | `AWSLambdaVPCAccessExecutionRole` + `s3:GetObject` on the bucket |

Network note: because the function sits in private subnets it reaches S3 through the NAT Gateway (or an S3 gateway endpoint).

Build and deploy:

```bash
./build.sh
aws lambda update-function-code --function-name DataShield-S3-to-RDS \
  --zip-file fileb://DataShield-Lambda.zip --region ap-southeast-2
```

Windows (as used originally): `Compress-Archive -Path * -DestinationPath DataShield-Lambda.zip -Force` from inside the package folder.
