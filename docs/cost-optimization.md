# Cost optimization / paused state

| Resource | Action when paused |
|---|---|
| Service ASG | min/desired = 0 |
| RDS | stop (AWS auto-starts it after 7 days) |
| Standalone EC2 (Collector, Analyzer, Archive, Bastion) | stop (EBS still billed) |
| NAT Gateway | delete; re-add `0.0.0.0/0 → NAT` to Private-NAT-RT on rebuild |
| ALB | delete; recreate listener, target groups and `/collect` rule |
| Keep | VPC, subnets, route tables, SGs, IAM, S3, Lambda, API GW, CloudFront, AMI, Launch Template |

Helpers: `scripts/pause_project.sh`, `scripts/resume_project.sh`.
