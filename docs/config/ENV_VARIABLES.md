# Environment Variables Reference

This document lists all environment variables used in Calibrify, their purposes, and example values.

## Core Settings

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `DJANGO_SETTINGS_MODULE` | Django settings module to use | Yes | - | `config.settings.production` |
| `SECRET_KEY` | Django secret key | Yes | - | `your-secret-key-here` |
| `DEBUG` | Debug mode flag | No | `False` | `True` |
| `ALLOWED_HOSTS` | Allowed host domains | Yes | - | `localhost,example.com` |

## Database Configuration

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `DB_NAME` | Database name | Yes | - | `calibrify_db` |
| `DB_USER` | Database user | Yes | - | `calibrify_user` |
| `DB_PASSWORD` | Database password | Yes | - | `your-secure-password` |
| `DB_HOST` | Database host | Yes | - | `db` |
| `DB_PORT` | Database port | No | `5432` | `5432` |

## Email Settings

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `EMAIL_HOST` | SMTP server host | Yes | - | `smtp.gmail.com` |
| `EMAIL_PORT` | SMTP server port | No | `587` | `587` |
| `EMAIL_HOST_USER` | SMTP username | Yes | - | `your@email.com` |
| `EMAIL_HOST_PASSWORD` | SMTP password | Yes | - | `your-app-password` |
| `EMAIL_USE_TLS` | Use TLS for email | No | `True` | `True` |
| `DEFAULT_FROM_EMAIL` | Default sender address | No | - | `noreply@example.com` |

## Security Settings

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `CSRF_TRUSTED_ORIGINS` | Trusted CSRF origins | No | - | `https://example.com` |
| `SECURE_SSL_REDIRECT` | Force SSL redirect | No | `True` | `True` |
| `SESSION_COOKIE_SECURE` | Secure session cookie | No | `True` | `True` |
| `CSRF_COOKIE_SECURE` | Secure CSRF cookie | No | `True` | `True` |

## Storage Settings

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `USE_S3` | Use S3 for storage | No | `False` | `True` |
| `AWS_ACCESS_KEY_ID` | AWS access key | If USE_S3 | - | `your-key-id` |
| `AWS_SECRET_ACCESS_KEY` | AWS secret key | If USE_S3 | - | `your-secret-key` |
| `AWS_STORAGE_BUCKET_NAME` | S3 bucket name | If USE_S3 | - | `calibrify-storage` |
| `AWS_S3_REGION_NAME` | AWS region | If USE_S3 | - | `us-east-1` |

## Cache Settings

| Variable | Description | Required | Default | Example |
|----------|-------------|----------|---------|---------|
| `REDIS_URL` | Redis connection URL | No | - | `redis://redis:6379/1` |
| `CACHE_TIMEOUT` | Cache timeout in seconds | No | `300` | `600` |

## Example .env File

```env
# Core Settings
DJANGO_SETTINGS_MODULE=config.settings.production
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=example.com,www.example.com

# Database
DB_NAME=calibrify_db
DB_USER=calibrify_user
DB_PASSWORD=your-secure-password
DB_HOST=db
DB_PORT=5432

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your@email.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
DEFAULT_FROM_EMAIL=noreply@example.com

# Security
CSRF_TRUSTED_ORIGINS=https://example.com
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True

# Storage
USE_S3=True
AWS_ACCESS_KEY_ID=your-key-id
AWS_SECRET_ACCESS_KEY=your-secret-key
AWS_STORAGE_BUCKET_NAME=calibrify-storage
AWS_S3_REGION_NAME=us-east-1

# Cache
REDIS_URL=redis://redis:6379/1
CACHE_TIMEOUT=600
```

## Notes

1. Never commit `.env` files to version control
2. Use different `.env` files for development and production
3. Keep production credentials secure and rotate them regularly
4. Use strong, unique passwords for all credentials
5. Consider using a secrets management service in production 