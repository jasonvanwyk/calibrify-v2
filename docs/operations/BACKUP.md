# Backup and Recovery Procedures

## Overview

This document outlines the backup and recovery procedures for Calibrify, ensuring data safety and business continuity.

## Backup Strategy

### 1. Database Backups

#### Daily Full Backups
```bash
#!/bin/bash
# /opt/calibrify/scripts/backup/daily-db-backup.sh

# Configuration
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/backups/calibrify/database"
RETENTION_DAYS=30
S3_BUCKET="calibrify-backups"

# Create backup
docker-compose -f docker/production/docker-compose.prod.yml exec -T db \
    pg_dump -U $DB_USER $DB_NAME | gzip > "$BACKUP_DIR/full_$TIMESTAMP.sql.gz"

# Upload to S3
aws s3 cp "$BACKUP_DIR/full_$TIMESTAMP.sql.gz" \
    "s3://$S3_BUCKET/database/daily/full_$TIMESTAMP.sql.gz"

# Cleanup old backups
find $BACKUP_DIR -type f -mtime +$RETENTION_DAYS -delete
```

#### Hourly WAL Archiving
```bash
# postgresql.conf
archive_mode = on
archive_command = 'test ! -f /var/lib/postgresql/archive/%f && cp %p /var/lib/postgresql/archive/%f'
archive_timeout = 3600
```

### 2. File Storage Backups

#### Media Files
```bash
#!/bin/bash
# /opt/calibrify/scripts/backup/media-backup.sh

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/backups/calibrify/media"
S3_BUCKET="calibrify-backups"

# Backup media files
tar -czf "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" /var/www/calibrify/media

# Upload to S3
aws s3 cp "$BACKUP_DIR/media_$TIMESTAMP.tar.gz" \
    "s3://$S3_BUCKET/media/media_$TIMESTAMP.tar.gz"
```

#### Configuration Files
```bash
#!/bin/bash
# /opt/calibrify/scripts/backup/config-backup.sh

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_DIR="/var/backups/calibrify/config"
S3_BUCKET="calibrify-backups"

# Backup configuration
tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
    /opt/calibrify/config \
    /etc/nginx/sites-available/calibrify.conf \
    /etc/systemd/system/calibrify*.service

# Upload to S3
aws s3 cp "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
    "s3://$S3_BUCKET/config/config_$TIMESTAMP.tar.gz"
```

## Backup Schedule

### 1. Database Backups
- Full backup: Daily at 1 AM UTC
- WAL archiving: Continuous
- Retention: 30 days local, 90 days in S3

### 2. File Backups
- Media files: Daily at 2 AM UTC
- Config files: On change
- Retention: 7 days local, 30 days in S3

## Recovery Procedures

### 1. Database Recovery

#### Full Database Restore
```bash
#!/bin/bash
# /opt/calibrify/scripts/recovery/restore-db.sh

# Stop application
docker-compose -f docker/production/docker-compose.prod.yml down

# Restore database
gunzip -c $BACKUP_FILE | \
    docker-compose -f docker/production/docker-compose.prod.yml exec -T db \
    psql -U $DB_USER $DB_NAME

# Start application
docker-compose -f docker/production/docker-compose.prod.yml up -d
```

#### Point-in-Time Recovery
```bash
# recovery.conf
restore_command = 'cp /var/lib/postgresql/archive/%f %p'
recovery_target_time = '2023-12-01 15:30:00'
```

### 2. File Recovery

#### Media Files Restore
```bash
#!/bin/bash
# /opt/calibrify/scripts/recovery/restore-media.sh

# Download from S3
aws s3 cp "s3://$S3_BUCKET/media/$BACKUP_FILE" .

# Extract files
tar -xzf $BACKUP_FILE -C /var/www/calibrify/media

# Fix permissions
chown -R www-data:www-data /var/www/calibrify/media
```

#### Configuration Restore
```bash
#!/bin/bash
# /opt/calibrify/scripts/recovery/restore-config.sh

# Download from S3
aws s3 cp "s3://$S3_BUCKET/config/$BACKUP_FILE" .

# Extract files
tar -xzf $BACKUP_FILE -C /

# Reload services
systemctl daemon-reload
systemctl restart nginx
```

## Backup Verification

### 1. Automated Verification

```python
# /opt/calibrify/scripts/backup/verify_backup.py

def verify_database_backup(backup_file):
    """Verify database backup integrity."""
    try:
        # Create temporary database
        temp_db = f"verify_{int(time.time())}"
        
        # Restore backup to temporary database
        subprocess.run([
            "createdb", temp_db,
            "-T", "template0"
        ])
        
        subprocess.run([
            "gunzip", "-c", backup_file,
            "|", "psql", temp_db
        ])
        
        # Run verification queries
        verify_queries = [
            "SELECT COUNT(*) FROM equipment",
            "SELECT COUNT(*) FROM calibrations",
            "SELECT COUNT(*) FROM users"
        ]
        
        for query in verify_queries:
            result = subprocess.run([
                "psql", temp_db,
                "-c", query
            ])
            if result.returncode != 0:
                raise Exception(f"Verification query failed: {query}")
        
        return True
        
    finally:
        # Cleanup
        subprocess.run(["dropdb", temp_db])
```

### 2. Manual Verification

Monthly checklist:
- [ ] Restore test database
- [ ] Verify data integrity
- [ ] Test application functionality
- [ ] Check file permissions
- [ ] Validate configuration

## Disaster Recovery

### 1. High-Level Recovery Plan

1. **Assessment**
   - Determine scope of data loss
   - Identify most recent valid backup
   - Estimate recovery time

2. **Communication**
   - Notify stakeholders
   - Update status page
   - Estimate downtime

3. **Recovery**
   - Restore infrastructure
   - Recover data
   - Verify integrity

4. **Validation**
   - Test functionality
   - Verify data consistency
   - Check integrations

### 2. Recovery Time Objectives

| Component | RTO | RPO |
|-----------|-----|-----|
| Database | 1 hour | 5 minutes |
| Media files | 4 hours | 24 hours |
| Configuration | 1 hour | On change |

## Monitoring

### 1. Backup Monitoring

```python
# /opt/calibrify/scripts/monitoring/backup_monitor.py

def check_backup_status():
    alerts = []
    
    # Check backup completion
    if not backup_completed_successfully():
        alerts.append({
            'level': 'critical',
            'message': 'Daily backup failed'
        })
    
    # Check backup size
    if backup_size_anomaly():
        alerts.append({
            'level': 'warning',
            'message': 'Unusual backup size detected'
        })
    
    # Check S3 sync
    if not s3_sync_verified():
        alerts.append({
            'level': 'warning',
            'message': 'S3 sync issue detected'
        })
    
    return alerts
```

### 2. Alert Configuration

```yaml
# prometheus-alerts.yml
groups:
  - name: backup
    rules:
      - alert: BackupFailed
        expr: backup_status != 1
        for: 1h
        labels:
          severity: critical
        annotations:
          summary: Backup failed
          description: Daily backup has failed
```

## Security Considerations

### 1. Encryption

```python
# Backup encryption configuration
BACKUP_ENCRYPTION = {
    'algorithm': 'AES-256-GCM',
    'key_rotation': 90,  # days
    'key_storage': 'aws-kms'
}
```

### 2. Access Control

```bash
# S3 bucket policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::ACCOUNT-ID:role/backup-role"
            },
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::calibrify-backups/*"
        }
    ]
}
```

## Maintenance

### 1. Backup Cleanup

```bash
#!/bin/bash
# /opt/calibrify/scripts/maintenance/cleanup-backups.sh

# Clean local backups
find /var/backups/calibrify -type f -mtime +30 -delete

# Clean S3 backups
aws s3 ls s3://$S3_BUCKET/database/ \
    --recursive \
    | while read -r line; do
        createDate=$(echo $line|awk {'print $1'})
        if [[ $createDate < $(date -d '90 days ago' +%Y-%m-%d) ]]; then
            aws s3 rm "s3://$S3_BUCKET/$(echo $line|awk {'print $4'})"
        fi
    done
```

### 2. Performance Optimization

```bash
# postgresql.conf backup settings
maintenance_work_mem = 1GB
max_wal_size = 4GB
checkpoint_completion_target = 0.9
```

## Documentation

### 1. Backup Inventory

Maintain a catalog of backups:
```sql
CREATE TABLE backup_inventory (
    id SERIAL PRIMARY KEY,
    backup_type VARCHAR(50),
    filename VARCHAR(255),
    created_at TIMESTAMP,
    size_bytes BIGINT,
    checksum VARCHAR(64),
    status VARCHAR(20),
    location VARCHAR(255)
);
```

### 2. Recovery Runbook

Document step-by-step recovery procedures:
1. Assess the situation
2. Select appropriate backup
3. Follow recovery procedure
4. Verify restoration
5. Document the incident 