# Security Policies and Procedures

## Overview

This document outlines the security policies and procedures for the Calibrify application. Following these guidelines is crucial for maintaining the security and integrity of the system.

## Security Architecture

### 1. Authentication

#### JWT Implementation
```python
# JWT Configuration
JWT_AUTH = {
    'JWT_SECRET_KEY': env('JWT_SECRET_KEY'),
    'JWT_ALGORITHM': 'HS256',
    'JWT_EXPIRATION_DELTA': timedelta(hours=1),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}
```

#### Password Policies
- Minimum 12 characters
- Must include:
  - Uppercase letters
  - Lowercase letters
  - Numbers
  - Special characters
- Password history: Last 5 passwords
- Maximum age: 90 days

### 2. Authorization

#### Role-Based Access Control (RBAC)
```python
ROLES = {
    'ADMIN': {
        'permissions': ['*'],
    },
    'MANAGER': {
        'permissions': [
            'equipment.view',
            'equipment.add',
            'equipment.edit',
            'calibration.manage',
        ],
    },
    'TECHNICIAN': {
        'permissions': [
            'equipment.view',
            'calibration.view',
            'calibration.perform',
        ],
    },
}
```

#### Object-Level Permissions
```python
class Equipment(models.Model):
    def has_permission(self, user, action):
        if user.role == 'ADMIN':
            return True
        if action == 'view':
            return True
        return user.has_permission(f'equipment.{action}')
```

### 3. Data Protection

#### Encryption at Rest
- Database encryption
- File storage encryption
- Secure key management

#### Encryption in Transit
- TLS 1.3 required
- Strong cipher suites
- Certificate management

## Security Controls

### 1. Input Validation

```python
class EquipmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[\w\-\s]+$',
                message='Name contains invalid characters'
            )
        ]
    )
    serial_number = serializers.CharField(
        max_length=50,
        validators=[
            RegexValidator(
                regex=r'^[A-Z0-9\-]+$',
                message='Invalid serial number format'
            )
        ]
    )
```

### 2. Rate Limiting

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'login': '5/minute',
    }
}
```

### 3. Session Management

```python
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Strict'
SESSION_EXPIRE_AT_BROWSER_CLOSE = True
SESSION_COOKIE_AGE = 3600  # 1 hour
```

## Security Monitoring

### 1. Logging

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'security.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'security': {
            'handlers': ['security_file'],
            'level': 'INFO',
            'propagate': True,
        }
    }
}
```

### 2. Audit Trail

```python
class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    action = models.CharField(max_length=50)
    resource_type = models.CharField(max_length=50)
    resource_id = models.CharField(max_length=50)
    details = models.JSONField()
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
```

## Incident Response

### 1. Security Incident Procedure

1. **Detection & Analysis**
   - Log monitoring
   - Alert investigation
   - Impact assessment

2. **Containment**
   - Account suspension
   - System isolation
   - Evidence preservation

3. **Eradication**
   - Vulnerability patching
   - System hardening
   - Security updates

4. **Recovery**
   - Service restoration
   - Data verification
   - System monitoring

### 2. Incident Reporting

```python
def report_security_incident(incident_type, details):
    incident = SecurityIncident.objects.create(
        type=incident_type,
        details=details,
        status='OPEN'
    )
    
    # Notify security team
    notify_security_team(incident)
    
    # Log incident
    logger.critical(f"Security incident: {incident_type}")
    
    return incident
```

## Compliance Requirements

### 1. Data Retention

- Equipment records: 7 years
- Calibration certificates: 10 years
- Audit logs: 5 years
- Security incidents: 3 years

### 2. Privacy Compliance

#### GDPR Requirements
- Data minimization
- Purpose limitation
- Storage limitation
- User consent management

#### Data Subject Rights
- Right to access
- Right to rectification
- Right to erasure
- Right to portability

## Security Testing

### 1. Automated Testing

```python
class SecurityTests(TestCase):
    def test_password_complexity(self):
        weak_passwords = [
            'password123',
            'abc123',
            'qwerty'
        ]
        for password in weak_passwords:
            with self.assertRaises(ValidationError):
                validate_password(password)

    def test_jwt_expiration(self):
        token = create_jwt_token(user)
        self.assertTrue(token_is_valid(token))
        
        # Fast forward time
        with freeze_time(timezone.now() + timedelta(hours=2)):
            self.assertFalse(token_is_valid(token))
```

### 2. Penetration Testing

Annual security assessment including:
- Vulnerability scanning
- Penetration testing
- Security code review
- Configuration review

## Deployment Security

### 1. Environment Security

```bash
# Security headers in nginx
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header Content-Security-Policy "default-src 'self';" always;
```

### 2. Container Security

```dockerfile
# Security-focused Dockerfile
FROM python:3.11-slim

# Run as non-root user
RUN useradd -m -s /bin/bash app
USER app

# Security updates
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get clean

# Remove unnecessary tools
RUN apt-get remove -y curl wget
```

## Security Checklist

### 1. Pre-Deployment
- [ ] Security scanning completed
- [ ] Dependencies updated
- [ ] Secrets rotated
- [ ] Permissions verified
- [ ] SSL certificates valid

### 2. Regular Maintenance
- [ ] Security patches applied
- [ ] Access reviews conducted
- [ ] Logs analyzed
- [ ] Backups verified
- [ ] Monitoring active

## Emergency Contacts

### Security Team
- Primary: security@example.com
- Emergency: +1-234-567-8900
- On-call: https://oncall.example.com

### External Resources
- Cloud Provider Support
- Security Consultants
- Legal Team
- PR Team 