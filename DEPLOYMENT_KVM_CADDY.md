# Django CRM Deployment Guide - KVM + Caddy

Complete guide for deploying Django CRM on a KVM server with Caddy as reverse proxy.

---

## 📋 Prerequisites

- KVM server running Ubuntu 22.04/24.04 or Debian 11/12
- Root or sudo access
- Domain name pointing to your server IP
- At least 2GB RAM, 20GB disk space
- Basic Linux command line knowledge

---

## 🚀 Step 1: Server Initial Setup

### 1.1 Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 1.2 Create Application User

```bash
# Create user for running the application
sudo useradd -m -s /bin/bash django
sudo passwd django  # Set a strong password

# Add to sudo group (optional, for maintenance)
sudo usermod -aG sudo django

# Switch to django user
sudo su - django
```

### 1.3 Install System Dependencies

```bash
sudo apt install -y \
    python3 python3-pip python3-venv \
    postgresql postgresql-contrib \
    git curl wget \
    build-essential \
    libpq-dev \
    redis-server \
    supervisor
```

---

## 🗄️ Step 2: Database Setup (PostgreSQL)

### 2.1 Create Database and User

```bash
# Switch to postgres user
sudo -u postgres psql

# In PostgreSQL prompt:
CREATE DATABASE django_crm;
CREATE USER django_user WITH PASSWORD 'your_strong_password_here';
ALTER ROLE django_user SET client_encoding TO 'utf8';
ALTER ROLE django_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE django_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE django_crm TO django_user;

# PostgreSQL 15+ requires additional grant
\c django_crm
GRANT ALL ON SCHEMA public TO django_user;

# Exit
\q
```

### 2.2 Configure PostgreSQL

```bash
# Allow password authentication
sudo nano /etc/postgresql/15/main/pg_hba.conf

# Change this line:
# local   all             all                                     peer
# To:
local   all             all                                     md5

# Restart PostgreSQL
sudo systemctl restart postgresql
```

---

## 📦 Step 3: Deploy Django Application

### 3.1 Clone Repository

```bash
# As django user
cd /home/django
git clone https://github.com/radoslav1992/django_crm.git
cd django_crm
```

### 3.2 Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3.3 Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
```

### 3.4 Configure Environment Variables

```bash
# Create .env file
nano .env
```

Add the following (replace with your actual values):

```bash
# Django Settings
SECRET_KEY=your-very-long-random-secret-key-here-generate-with-django
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database Configuration
DATABASE_URL=postgresql://django_user:your_strong_password_here@localhost/django_crm

# Email Configuration (Resend)
RESEND_API_KEY=re_your_resend_api_key
RESEND_FROM_EMAIL=noreply@yourdomain.com
RESEND_FROM_NAME=Your Company Name

# Payment Configuration (Stripe)
STRIPE_SECRET_KEY=sk_live_your_stripe_secret_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_publishable_key
STRIPE_WEBHOOK_SECRET=whsec_your_webhook_secret

# AI Configuration (Google Gemini)
GEMINI_API_KEY=AIzaSy_your_gemini_api_key

# Site Configuration
SITE_URL=https://yourdomain.com

# Security (for production)
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**Generate SECRET_KEY:**
```bash
python3 -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### 3.5 Run Migrations

```bash
source venv/bin/activate
python manage.py migrate
```

### 3.6 Create Superuser

```bash
python manage.py createsuperuser
```

### 3.7 Load FAQ Data

```bash
python manage.py load_faq
```

### 3.8 Collect Static Files

```bash
python manage.py collectstatic --noinput
```

### 3.9 Test Application

```bash
# Test that it runs
python manage.py runserver 0.0.0.0:8000

# Press Ctrl+C to stop
```

---

## 🔧 Step 4: Configure Gunicorn

### 4.1 Create Gunicorn Configuration

```bash
mkdir -p /home/django/django_crm/config/gunicorn
nano /home/django/django_crm/config/gunicorn/gunicorn_config.py
```

Add:

```python
import multiprocessing

bind = "127.0.0.1:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2

# Logging
accesslog = "/home/django/django_crm/logs/gunicorn-access.log"
errorlog = "/home/django/django_crm/logs/gunicorn-error.log"
loglevel = "info"

# Process naming
proc_name = "django_crm"

# Server mechanics
daemon = False
pidfile = "/home/django/django_crm/gunicorn.pid"
user = "django"
group = "django"
```

### 4.2 Create Log Directory

```bash
mkdir -p /home/django/django_crm/logs
```

### 4.3 Create Systemd Service

```bash
sudo nano /etc/systemd/system/django_crm.service
```

Add:

```ini
[Unit]
Description=Django CRM Gunicorn Application
After=network.target postgresql.service redis.service

[Service]
Type=notify
User=django
Group=django
WorkingDirectory=/home/django/django_crm
Environment="PATH=/home/django/django_crm/venv/bin"
ExecStart=/home/django/django_crm/venv/bin/gunicorn \
    --config /home/django/django_crm/config/gunicorn/gunicorn_config.py \
    config.wsgi:application
ExecReload=/bin/kill -s HUP $MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 4.4 Enable and Start Service

```bash
sudo systemctl daemon-reload
sudo systemctl enable django_crm
sudo systemctl start django_crm
sudo systemctl status django_crm
```

Check logs if needed:
```bash
sudo journalctl -u django_crm -f
```

---

## 🌐 Step 5: Install and Configure Caddy

### 5.1 Install Caddy

```bash
# Install Caddy (official method)
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
sudo apt update
sudo apt install caddy
```

### 5.2 Configure Caddy

```bash
sudo nano /etc/caddy/Caddyfile
```

Replace contents with:

```caddy
# Django CRM Configuration
yourdomain.com, www.yourdomain.com {
    # Automatic HTTPS
    # Caddy will automatically obtain and renew SSL certificates

    # Request logging
    log {
        output file /var/log/caddy/django_crm_access.log
        format json
    }

    # Handle errors
    handle_errors {
        @404 {
            expression {http.error.status_code} == 404
        }
        rewrite @404 /404.html
    }

    # Static files
    handle /static/* {
        root * /home/django/django_crm/staticfiles
        file_server
        
        # Cache static files for 1 year
        header Cache-Control "public, max-age=31536000, immutable"
    }

    # Media files
    handle /media/* {
        root * /home/django/django_crm/media
        file_server
        
        # Cache media files for 1 month
        header Cache-Control "public, max-age=2592000"
    }

    # Proxy all other requests to Gunicorn
    reverse_proxy 127.0.0.1:8000 {
        # Health check
        health_uri /health/
        health_interval 30s
        health_timeout 5s
        
        # Headers
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
        header_up X-Forwarded-Host {host}
    }

    # Security headers
    header {
        # Enable HSTS
        Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
        
        # Prevent clickjacking
        X-Frame-Options "SAMEORIGIN"
        
        # Prevent MIME type sniffing
        X-Content-Type-Options "nosniff"
        
        # XSS Protection
        X-XSS-Protection "1; mode=block"
        
        # Referrer Policy
        Referrer-Policy "strict-origin-when-cross-origin"
        
        # Content Security Policy (adjust as needed)
        Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net https://code.jquery.com; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; img-src 'self' data: https:; font-src 'self' https://cdn.jsdelivr.net; connect-src 'self';"
        
        # Remove server identification
        -Server
    }

    # Compress responses
    encode gzip zstd

    # Rate limiting (optional, adjust as needed)
    rate_limit {
        zone dynamic {
            key {remote_host}
            events 100
            window 1m
        }
    }
}

# Redirect www to non-www (or vice versa)
# Uncomment if you prefer www:
# www.yourdomain.com {
#     redir https://yourdomain.com{uri} permanent
# }

# Optional: Redirect HTTP to HTTPS (Caddy does this automatically)
```

**Important**: Replace `yourdomain.com` with your actual domain!

### 5.3 Create Log Directory

```bash
sudo mkdir -p /var/log/caddy
sudo chown caddy:caddy /var/log/caddy
```

### 5.4 Test and Start Caddy

```bash
# Test configuration
sudo caddy validate --config /etc/caddy/Caddyfile

# Reload Caddy
sudo systemctl reload caddy

# Check status
sudo systemctl status caddy

# View logs
sudo journalctl -u caddy -f
```

---

## 🔐 Step 6: Configure Firewall

### 6.1 UFW Firewall Setup

```bash
# Install UFW if not already installed
sudo apt install ufw

# Allow SSH (IMPORTANT: Do this first!)
sudo ufw allow 22/tcp

# Allow HTTP and HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

---

## 🔄 Step 7: Setup Celery for Background Tasks

### 7.1 Create Celery Service

```bash
sudo nano /etc/systemd/system/django_crm_celery.service
```

Add:

```ini
[Unit]
Description=Django CRM Celery Worker
After=network.target redis.service

[Service]
Type=forking
User=django
Group=django
WorkingDirectory=/home/django/django_crm
Environment="PATH=/home/django/django_crm/venv/bin"
ExecStart=/home/django/django_crm/venv/bin/celery -A config worker \
    --loglevel=info \
    --logfile=/home/django/django_crm/logs/celery.log \
    --pidfile=/home/django/django_crm/celery.pid
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 7.2 Create Celery Beat Service (for scheduled tasks)

```bash
sudo nano /etc/systemd/system/django_crm_celerybeat.service
```

Add:

```ini
[Unit]
Description=Django CRM Celery Beat
After=network.target redis.service

[Service]
Type=simple
User=django
Group=django
WorkingDirectory=/home/django/django_crm
Environment="PATH=/home/django/django_crm/venv/bin"
ExecStart=/home/django/django_crm/venv/bin/celery -A config beat \
    --loglevel=info \
    --logfile=/home/django/django_crm/logs/celerybeat.log \
    --pidfile=/home/django/django_crm/celerybeat.pid \
    --schedule=/home/django/django_crm/celerybeat-schedule
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
```

### 7.3 Enable and Start Services

```bash
sudo systemctl daemon-reload
sudo systemctl enable django_crm_celery django_crm_celerybeat
sudo systemctl start django_crm_celery django_crm_celerybeat
sudo systemctl status django_crm_celery
sudo systemctl status django_crm_celerybeat
```

---

## 📊 Step 8: Monitoring and Maintenance

### 8.1 Setup Log Rotation

```bash
sudo nano /etc/logrotate.d/django_crm
```

Add:

```
/home/django/django_crm/logs/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    create 0640 django django
    sharedscripts
    postrotate
        systemctl reload django_crm > /dev/null 2>&1 || true
    endscript
}

/var/log/caddy/*.log {
    daily
    rotate 14
    compress
    delaycompress
    notifempty
    missingok
    create 0640 caddy caddy
    sharedscripts
    postrotate
        systemctl reload caddy > /dev/null 2>&1 || true
    endscript
}
```

### 8.2 Create Backup Script

```bash
nano /home/django/backup_django_crm.sh
```

Add:

```bash
#!/bin/bash

# Configuration
BACKUP_DIR="/home/django/backups"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="django_crm"
DB_USER="django_user"
APP_DIR="/home/django/django_crm"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
pg_dump -U $DB_USER $DB_NAME | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# Backup media files
tar -czf $BACKUP_DIR/media_$DATE.tar.gz -C $APP_DIR media/

# Backup .env file
cp $APP_DIR/.env $BACKUP_DIR/env_$DATE

# Remove backups older than 30 days
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

Make executable:
```bash
chmod +x /home/django/backup_django_crm.sh
```

Add to crontab:
```bash
crontab -e

# Add this line (daily backup at 2 AM):
0 2 * * * /home/django/backup_django_crm.sh >> /home/django/backup.log 2>&1
```

### 8.3 Monitoring Commands

```bash
# Check all services
sudo systemctl status django_crm caddy django_crm_celery django_crm_celerybeat

# View application logs
sudo journalctl -u django_crm -f

# View Caddy logs
sudo journalctl -u caddy -f

# View access logs
tail -f /var/log/caddy/django_crm_access.log

# View Gunicorn logs
tail -f /home/django/django_crm/logs/gunicorn-error.log

# Check disk usage
df -h

# Check memory usage
free -h

# Check running processes
ps aux | grep gunicorn
```

---

## 🔄 Step 9: Deployment Updates

### 9.1 Create Deployment Script

```bash
nano /home/django/deploy.sh
```

Add:

```bash
#!/bin/bash

set -e

echo "🚀 Starting deployment..."

# Navigate to project directory
cd /home/django/django_crm

# Activate virtual environment
source venv/bin/activate

# Pull latest code
echo "📥 Pulling latest code..."
git pull origin main

# Install/update dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "📁 Collecting static files..."
python manage.py collectstatic --noinput

# Reload services
echo "🔄 Reloading services..."
sudo systemctl reload django_crm
sudo systemctl reload caddy
sudo systemctl restart django_crm_celery django_crm_celerybeat

echo "✅ Deployment complete!"
```

Make executable:
```bash
chmod +x /home/django/deploy.sh
```

### 9.2 Deploy Updates

```bash
cd /home/django
./deploy.sh
```

---

## 🔍 Step 10: Health Checks and Testing

### 10.1 Test Website

```bash
# Test from server
curl -I https://yourdomain.com

# Test HTTPS redirect
curl -I http://yourdomain.com

# Test static files
curl -I https://yourdomain.com/static/css/style.css
```

### 10.2 Check SSL Certificate

```bash
# Check certificate details
echo | openssl s_client -servername yourdomain.com -connect yourdomain.com:443 2>/dev/null | openssl x509 -noout -dates
```

### 10.3 Performance Test

```bash
# Install Apache Bench
sudo apt install apache2-utils

# Run simple load test
ab -n 100 -c 10 https://yourdomain.com/
```

---

## 🛡️ Step 11: Security Hardening

### 11.1 Configure Fail2Ban

```bash
# Install Fail2Ban
sudo apt install fail2ban

# Create configuration
sudo nano /etc/fail2ban/jail.local
```

Add:

```ini
[DEFAULT]
bantime = 1h
findtime = 10m
maxretry = 5

[sshd]
enabled = true

[caddy-auth]
enabled = true
port = http,https
logpath = /var/log/caddy/*.log
maxretry = 5
```

Start Fail2Ban:
```bash
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 11.2 Setup Automatic Security Updates

```bash
sudo apt install unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 11.3 Disable Root Login

```bash
sudo nano /etc/ssh/sshd_config

# Change:
PermitRootLogin no
PasswordAuthentication no  # If using SSH keys

# Restart SSH
sudo systemctl restart sshd
```

---

## 📝 Step 12: Final Checklist

### Pre-Launch Checklist:

- [ ] Domain DNS configured and propagated
- [ ] PostgreSQL database created and configured
- [ ] All environment variables set in `.env`
- [ ] Migrations run successfully
- [ ] Superuser created
- [ ] FAQ data loaded
- [ ] Static files collected
- [ ] Gunicorn service running
- [ ] Caddy service running and SSL active
- [ ] Celery workers running
- [ ] Firewall configured
- [ ] Backups configured
- [ ] Monitoring setup
- [ ] Security hardening complete
- [ ] Test email sending (Resend)
- [ ] Test payment processing (Stripe)
- [ ] Test AI features (Gemini)
- [ ] All pages load correctly
- [ ] Mobile responsive working
- [ ] FAQ accessible
- [ ] Admin panel accessible

### Post-Launch Monitoring:

- [ ] Check error logs daily
- [ ] Monitor disk space
- [ ] Check backup logs
- [ ] Review access logs
- [ ] Monitor SSL certificate expiry (Caddy auto-renews)
- [ ] Check application performance
- [ ] Review user feedback

---

## 🆘 Troubleshooting

### Issue: Site not accessible

```bash
# Check if Caddy is running
sudo systemctl status caddy

# Check if Gunicorn is running
sudo systemctl status django_crm

# Check firewall
sudo ufw status

# Check DNS
nslookup yourdomain.com
```

### Issue: 502 Bad Gateway

```bash
# Check Gunicorn logs
tail -f /home/django/django_crm/logs/gunicorn-error.log

# Restart Gunicorn
sudo systemctl restart django_crm
```

### Issue: Static files not loading

```bash
# Recollect static files
cd /home/django/django_crm
source venv/bin/activate
python manage.py collectstatic --noinput

# Check permissions
ls -la /home/django/django_crm/staticfiles
```

### Issue: Database connection error

```bash
# Check PostgreSQL is running
sudo systemctl status postgresql

# Test database connection
sudo -u postgres psql -d django_crm -U django_user

# Check .env file has correct credentials
cat /home/django/django_crm/.env | grep DATABASE_URL
```

### Issue: SSL certificate not working

```bash
# Check Caddy logs
sudo journalctl -u caddy -n 50

# Manually reload Caddy
sudo systemctl reload caddy

# Caddy automatically obtains certificates, but ensure:
# - Port 80 and 443 are open
# - Domain points to your server
# - No other service is using port 80/443
```

---

## 🎉 Congratulations!

Your Django CRM is now deployed on KVM with Caddy!

### Access Your Application:

- **Website**: https://yourdomain.com
- **Admin**: https://yourdomain.com/admin
- **FAQ**: https://yourdomain.com/faq

### Useful Commands:

```bash
# Restart all services
sudo systemctl restart django_crm caddy django_crm_celery django_crm_celerybeat

# View all logs
sudo journalctl -u django_crm -u caddy -f

# Deploy updates
cd /home/django && ./deploy.sh

# Manual backup
cd /home/django && ./backup_django_crm.sh
```

---

**Need help?** Check the FAQ at `/faq/` or review logs for errors.

**Good luck with your launch!** 🚀

