#!/bin/bash
# Cost-saving "paused" state (see docs/cost-optimization.md).
# Review each step - NAT Gateway and ALB are DELETED and must be recreated on resume.
set -euo pipefail
R="${AWS_REGION:-ap-southeast-2}"
echo "1) ASG -> 0"
aws autoscaling update-auto-scaling-group --auto-scaling-group-name DataShield-Service-ASG \
  --min-size 0 --desired-capacity 0 --region "$R"
echo "2) Stop standalone EC2 (set IDs)"
: "${INSTANCE_IDS:?export INSTANCE_IDS=\"i-aaa i-bbb ...\"}"
aws ec2 stop-instances --instance-ids $INSTANCE_IDS --region "$R"
echo "3) Stop RDS (auto-restarts after 7 days)"
aws rds stop-db-instance --db-instance-identifier datashield-rds-mysql --region "$R"
echo "Manual: delete NAT Gateway and ALB if not demoing (console or CLI)."
