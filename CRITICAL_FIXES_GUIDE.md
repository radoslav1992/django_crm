# 🚨 Critical Production Fixes - Implementation Guide

**IMPORTANT**: These fixes MUST be implemented before production deployment.

---

## 1. Create `.env.example` File (5 minutes)

Create file: `.env.example` in project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here-generate-with-django-get-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database (Production - PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/django_crm

# Stripe Configuration (Platform Subscriptions)
STRIPE_PUBLISHABLE_KEY=pk_live_your_key_here
STRIPE_SECRET_KEY=sk_live_your_key_here
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret_here

# Stripe Price IDs
STRIPE_PRICE_BASIC=price_xxxxxxxxxxxxx
STRIPE_PRICE_PRO=price_xxxxxxxxxxxxx
STRIPE_PRICE_ENTERPRISE=price_xxxxxxxxxxxxx

# Google Gemini AI
GEMINI_API_KEY=your_gemini_api_key_here

# Redis (for Celery and Caching)
REDIS_URL=redis://localhost:6379/0

# Email Configuration
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-specific-password

# Language
LANGUAGE_CODE=bg

# Sentry (Error Monitoring - Optional)
SENTRY_DSN=
```

---

## 2. Add Production Security Settings (15 minutes)

### Add to `config/settings.py` (after line 20):

```python
# Production Security Settings
if not DEBUG:
    # Require HTTPS
    SECURE_SSL_REDIRECT = os.getenv('SECURE_SSL_REDIRECT', 'True') == 'True'
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # HSTS Settings
    SECURE_HSTS_SECONDS = int(os.getenv('SECURE_HSTS_SECONDS', '31536000'))
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookie Security
    SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
    CSRF_COOKIE_SECURE = os.getenv('CSRF_COOKIE_SECURE', 'True') == 'True'
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    
    # Browser Security
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Fail if SECRET_KEY is default in production
if not DEBUG and SECRET_KEY == 'django-insecure-change-this-in-production':
    raise ValueError("SECRET_KEY must be set in production! Generate one with: python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'")

# Fail if critical API keys missing
if not DEBUG:
    missing_keys = []
    if not STRIPE_SECRET_KEY:
        missing_keys.append('STRIPE_SECRET_KEY')
    if not STRIPE_WEBHOOK_SECRET:
        missing_keys.append('STRIPE_WEBHOOK_SECRET')
    if not GEMINI_API_KEY:
        missing_keys.append('GEMINI_API_KEY')
    
    if missing_keys:
        raise ValueError(f"Missing required environment variables in production: {', '.join(missing_keys)}")
```

---

## 3. Add Logging Configuration (10 minutes)

### Add to `config/settings.py` (at the end):

```python
# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 15,  # 15MB
            'backupCount': 10,
            'formatter': 'verbose',
        },
        'security_file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'security.log',
            'maxBytes': 1024 * 1024 * 15,
            'backupCount': 10,
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['security_file'],
            'level': 'WARNING',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory
import os
os.makedirs(BASE_DIR / 'logs', exist_ok=True)
```

---

## 4. Configure PostgreSQL (10 minutes)

### Update `config/settings.py` DATABASES section:

```python
import dj_database_url

# Database
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}
```

### Add to `requirements.txt`:

```
dj-database-url==2.1.0
```

### Then run:

```bash
pip install dj-database-url
```

---

## 5. Add Health Check Endpoint (15 minutes)

### Create `apps/accounts/health.py`:

```python
from django.http import JsonResponse
from django.db import connection
from django.core.cache import cache
import redis
from django.conf import settings


def health_check(request):
    """Health check endpoint for load balancers"""
    health = {
        'status': 'healthy',
        'checks': {}
    }
    
    # Check database
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        health['checks']['database'] = 'ok'
    except Exception as e:
        health['status'] = 'unhealthy'
        health['checks']['database'] = f'error: {str(e)}'
    
    # Check Redis
    try:
        r = redis.from_url(settings.CELERY_BROKER_URL)
        r.ping()
        health['checks']['redis'] = 'ok'
    except Exception as e:
        health['status'] = 'unhealthy'
        health['checks']['redis'] = f'error: {str(e)}'
    
    status_code = 200 if health['status'] == 'healthy' else 503
    return JsonResponse(health, status=status_code)
```

### Add to `config/urls.py`:

```python
from apps.accounts.health import health_check

urlpatterns = [
    path('health/', health_check, name='health_check'),
    # ... rest of urls
]
```

---

## 6. Add File Upload Validation (20 minutes)

### Create `apps/accounts/validators.py`:

```python
from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions
import magic  # python-magic


def validate_image_file(file):
    """Validate uploaded image files"""
    # Check file size (max 5MB)
    if file.size > 5 * 1024 * 1024:
        raise ValidationError('Image file too large ( > 5MB )')
    
    # Check MIME type
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)  # Reset file pointer
    
    allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
    if mime not in allowed_types:
        raise ValidationError(f'Unsupported file type: {mime}')
    
    # Check image dimensions
    try:
        w, h = get_image_dimensions(file)
        if w > 4000 or h > 4000:
            raise ValidationError('Image dimensions too large (max 4000x4000)')
    except:
        raise ValidationError('Invalid image file')


def validate_document_file(file):
    """Validate uploaded document files"""
    # Check file size (max 10MB)
    if file.size > 10 * 1024 * 1024:
        raise ValidationError('File too large ( > 10MB )')
    
    # Check MIME type
    mime = magic.from_buffer(file.read(1024), mime=True)
    file.seek(0)
    
    allowed_types = ['application/pdf', 'application/msword', 
                     'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
    if mime not in allowed_types:
        raise ValidationError(f'Unsupported file type: {mime}')
```

### Add to `requirements.txt`:

```
python-magic==0.4.27
```

### Update model fields to use validators:

```python
from apps.accounts.validators import validate_image_file

class DocumentTemplate(models.Model):
    logo = models.ImageField(
        upload_to='templates/logos/', 
        blank=True, 
        null=True,
        validators=[validate_image_file]
    )
```

---

## 7. Add Error Monitoring with Sentry (15 minutes)

### Install Sentry:

```bash
pip install sentry-sdk
```

### Add to `requirements.txt`:

```
sentry-sdk==1.38.0
```

### Add to `config/settings.py` (near the top, after imports):

```python
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Sentry Error Monitoring
SENTRY_DSN = os.getenv('SENTRY_DSN', '')

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1,  # 10% of transactions
        profiles_sample_rate=0.1,
        send_default_pii=False,  # Don't send user data
        environment='production' if not DEBUG else 'development',
    )
```

---

## 8. Add Database Backup Script (15 minutes)

### Create `scripts/backup_database.sh`:

```bash
#!/bin/bash

# Database Backup Script
BACKUP_DIR="/var/backups/django_crm"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="django_crm"

# Create backup directory
mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump -U postgres -d $DB_NAME -F c -f "$BACKUP_DIR/db_backup_$DATE.dump"

# Compress
gzip "$BACKUP_DIR/db_backup_$DATE.dump"

# Keep only last 7 days
find $BACKUP_DIR -name "db_backup_*.dump.gz" -mtime +7 -delete

echo "Backup completed: $BACKUP_DIR/db_backup_$DATE.dump.gz"
```

### Make executable:

```bash
chmod +x scripts/backup_database.sh
```

### Add to crontab (daily at 2 AM):

```bash
0 2 * * * /path/to/django_crm/scripts/backup_database.sh
```

---

## 9. Add API Rate Limiting (10 minutes)

### Update `config/settings.py` REST_FRAMEWORK:

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
    }
}
```

---

## 10. Add .gitignore entries (2 minutes)

### Ensure `.gitignore` contains:

```
# Environment
.env
.env.local
.env.production

# Logs
logs/
*.log

# Database
*.sqlite3
*.db

# Media files (optionally)
media/

# Backups
backups/
*.dump
*.dump.gz
```

---

## 🚀 Deployment Checklist

After implementing above fixes:

### 1. Environment Setup

```bash
# Copy .env.example to .env
cp .env.example .env

# Generate SECRET_KEY
python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'

# Edit .env with production values
nano .env
```

### 2. Database Migration

```bash
# Create PostgreSQL database
createdb django_crm

# Set DATABASE_URL in .env
DATABASE_URL=postgresql://user:pass@localhost/django_crm

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser
```

### 3. Static Files

```bash
python manage.py collectstatic --noinput
```

### 4. Test Services

```bash
# Test health endpoint
curl http://localhost:8000/health/

# Test email
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Test message', 'from@example.com', ['to@example.com'])

# Test Celery
celery -A config worker --loglevel=info
```

### 5. SSL Certificate

```bash
# Using Let's Encrypt
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### 6. Final Checks

- [ ] DEBUG=False in .env
- [ ] SECRET_KEY set to strong value
- [ ] ALLOWED_HOSTS set correctly
- [ ] Database backed up
- [ ] SSL certificate installed
- [ ] Sentry DSN configured
- [ ] Email service tested
- [ ] Stripe webhooks configured
- [ ] Health check responding
- [ ] Logs directory writable

---

## 📊 Estimated Time

- **Minimum fixes**: 1.5 hours
- **All fixes**: 2-3 hours
- **Testing**: 1 hour
- **Total**: 3-4 hours to production ready

---

## ⚠️ IMPORTANT NOTES

1. **Never commit `.env` file** - it contains secrets
2. **Always backup database** before migrations
3. **Test in staging** before production
4. **Monitor logs** after deployment
5. **Set up alerts** in Sentry

---

**Created**: October 7, 2025  
**Priority**: CRITICAL  
**Status**: Must implement before production

