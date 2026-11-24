-- DataShield RDS MySQL schema (MySQL 8.4)
-- Run from a host inside the VPC (e.g. the Service EC2 or via the Bastion):
--   mysql -h <rds-endpoint> -u admin -p < database/schema.sql

CREATE DATABASE IF NOT EXISTS datashield;
USE datashield;

-- Final table used by the Lambda (writer) and the Service tier (reader)
CREATE TABLE IF NOT EXISTS security_analysis (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    analysis_time   DATETIME DEFAULT CURRENT_TIMESTAMP,
    device_id       VARCHAR(100) NOT NULL,
    input_value     DECIMAL(10,2),
    processed_value DECIMAL(10,2),
    status          VARCHAR(50)  NOT NULL,
    result          TEXT
);

-- Optional connectivity test table used during early bring-up
CREATE TABLE IF NOT EXISTS test_connection (
    id            INT AUTO_INCREMENT PRIMARY KEY,
    instance_name VARCHAR(100),
    message       VARCHAR(255),
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Verification
-- SELECT id, analysis_time, device_id, input_value, processed_value, status
-- FROM security_analysis ORDER BY id DESC LIMIT 10;
