# Network design

Region `ap-southeast-2` (Sydney) · VPC `DataShield-VPC` · CIDR `10.60.0.0/16`

## Subnets

| Subnet | CIDR | AZ | Purpose |
|---|---|---|---|
| Public-Edge-Subnet-A | 10.60.1.0/24 | 2a | ALB, Bastion, NAT Gateway |
| Public-Edge-Subnet-B | 10.60.2.0/24 | 2b | ALB (second AZ) |
| Private-Collector-Subnet | 10.60.10.0/24 | 2a | Collector EC2 |
| Private-Analyzer-Subnet | 10.60.20.0/24 | 2a | Analyzer EC2 |
| Private-Service-Subnet | 10.60.30.0/24 | 2a | Service EC2 (ASG), Lambda ENIs |
| Private-Service-Subnet-B | 10.60.31.0/24 | 2b | Service EC2 (ASG), Lambda ENIs |
| Private-DB-Subnet | 10.60.40.0/24 | 2a | RDS |
| Private-DB-Subnet-B | 10.60.41.0/24 | 2b | RDS subnet group (2nd AZ) |
| Isolated-Archive-Subnet | 10.60.50.0/24 | 2a | Archive EC2 |

## Route tables

| Route table | Associated subnets | Default route |
|---|---|---|
| DataShield-Public-RT | Public-Edge-A/B | 0.0.0.0/0 → Internet Gateway |
| DataShield-Private-NAT-RT | Collector, Analyzer, Service, Service-B | 0.0.0.0/0 → NAT Gateway |
| DataShield-DB-RT | DB-A/B | none (local only) |
| DataShield-Archive-RT | Archive | none (local only) |

## Access & traffic matrix

| Source | Destination | Port | Allowed |
|---|---|---|---|
| Internet | ALB | 80/443 | Yes |
| API Gateway | ALB `/collect` | HTTP | Yes |
| ALB | Collector | 5000 | Yes |
| ALB | Service | 5000 | Yes |
| Collector | Analyzer | 5001 | Yes |
| Analyzer | S3 | 443 | Yes (instance IAM role) |
| Service | RDS | 3306 | Yes |
| Lambda | RDS | 3306 | Yes |
| Bastion | private EC2 | 22 | Yes |
| Internet | RDS / Archive | any | **No** |

## Security groups

| SG | Inbound |
|---|---|
| DataShield-ALB-SG | 80, 443 from internet |
| DataShield-Collector-SG | 5000 from ALB-SG; 22 from Bastion-SG |
| DataShield-Analyzer-SG | 5001 from Collector-SG; 22 from Bastion-SG |
| DataShield-Service-SG | 5000 from ALB-SG; 22 from Bastion-SG |
| DataShield-DB-SG | 3306 from Service-SG and Lambda-SG |
| DataShield-Lambda-SG | none |
| DataShield-Bastion-SG | 22 from your admin IP /32 only |
| DataShield-Archive-EC2 | 22 from Bastion/Collector paths only |

> Restrict Bastion SSH to your own current IP (`/32`). Do not publish your real IP in the repo.
