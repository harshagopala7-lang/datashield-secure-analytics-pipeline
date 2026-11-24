#!/bin/bash
# Restore after pause. NAT Gateway / ALB re-creation is manual (see docs/cost-optimization.md).
set -euo pipefail
R="${AWS_REGION:-ap-southeast-2}"
aws rds start-db-instance --db-instance-identifier datashield-rds-mysql --region "$R"
: "${INSTANCE_IDS:?export INSTANCE_IDS=\"i-aaa i-bbb ...\"}"
aws ec2 start-instances --instance-ids $INSTANCE_IDS --region "$R"
aws autoscaling update-auto-scaling-group --auto-scaling-group-name DataShield-Service-ASG \
  --min-size 2 --desired-capacity 2 --max-size 6 --region "$R"
