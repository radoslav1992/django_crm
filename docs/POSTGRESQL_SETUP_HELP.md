# PostgreSQL Setup Help

## Finding PostgreSQL Configuration

### Step 1: Find PostgreSQL Version

```bash
# Check installed PostgreSQL version
psql --version

# Or check what's running
sudo systemctl status postgresql

# Find all PostgreSQL versions installed
ls -la /etc/postgresql/
```

### Step 2: Find pg_hba.conf Location

```bash
# Connect to PostgreSQL and ask where the config is
sudo -u postgres psql -c "SHOW hba_file;"

# Or find it manually
sudo find /etc/postgresql -name pg_hba.conf

# Common locations:
# Ubuntu/Debian: /etc/postgresql/{version}/main/pg_hba.conf
# - Version 12: /etc/postgresql/12/main/pg_hba.conf
# - Version 13: /etc/postgresql/13/main/pg_hba.conf
# - Version 14: /etc/postgresql/14/main/pg_hba.conf
# - Version 15: /etc/postgresql/15/main/pg_hba.conf
# - Version 16: /etc/postgresql/16/main/pg_hba.conf
```

---

## Complete pg_hba.conf Template

If the file is empty or you need to recreate it, here's a complete template:

```bash
# PostgreSQL Client Authentication Configuration File
# ===================================================
#
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             postgres                                peer
local   all             all                                     md5

# IPv4 local connections:
host    all             all             127.0.0.1/32            md5
host    all             all             0.0.0.0/0               md5

# IPv6 local connections:
host    all             all             ::1/128                 md5

# Allow replication connections from localhost, by a user with the
# replication privilege.
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
```

### What This Means:

- **`local all postgres peer`** - PostgreSQL user can connect locally without password
- **`local all all md5`** - All other local users need password
- **`host all all 127.0.0.1/32 md5`** - Local TCP connections need password
- **`host all all 0.0.0.0/0 md5`** - Remote connections allowed (use with caution!)

---

## Quick Setup Commands

### Option 1: Auto-detect and Configure

```bash
#!/bin/bash

# Find PostgreSQL version
PG_VERSION=$(psql --version | grep -oP '\d+' | head -1)
echo "PostgreSQL version: $PG_VERSION"

# Find pg_hba.conf location
HBA_FILE=$(sudo -u postgres psql -t -c "SHOW hba_file;" | xargs)
echo "pg_hba.conf location: $HBA_FILE"

# Backup existing file
sudo cp "$HBA_FILE" "${HBA_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

# Edit the file
sudo nano "$HBA_FILE"
```

### Option 2: Direct Version-Specific Commands

```bash
# For PostgreSQL 16
sudo nano /etc/postgresql/16/main/pg_hba.conf

# For PostgreSQL 15
sudo nano /etc/postgresql/15/main/pg_hba.conf

# For PostgreSQL 14
sudo nano /etc/postgresql/14/main/pg_hba.conf

# For PostgreSQL 13
sudo nano /etc/postgresql/13/main/pg_hba.conf

# For PostgreSQL 12
sudo nano /etc/postgresql/12/main/pg_hba.conf
```

---

## What to Change for Django

### Minimal Configuration (Recommended for Production)

Find this line:
```
local   all             all                                     peer
```

Change it to:
```
local   all             all                                     md5
```

Or if the file is empty, add these lines:

```bash
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# Allow postgres user to connect without password (for admin)
local   all             postgres                                peer

# All other local connections require password
local   all             all                                     md5

# TCP/IP connections require password
host    all             all             127.0.0.1/32            md5
host    all             all             ::1/128                 md5
```

### After Editing:

```bash
# Test configuration
sudo -u postgres psql -c "SELECT version();"

# Restart PostgreSQL
sudo systemctl restart postgresql

# Check status
sudo systemctl status postgresql

# Test connection with your Django user
psql -U django_user -d django_crm -h localhost
# (it will ask for password - this is good!)
```

---

## Troubleshooting

### Issue: "File not found"

```bash
# Check if PostgreSQL is installed
dpkg -l | grep postgresql

# If not installed:
sudo apt update
sudo apt install postgresql postgresql-contrib

# Then find the config
sudo -u postgres psql -c "SHOW hba_file;"
```

### Issue: "Permission denied"

```bash
# Make sure you use sudo
sudo nano /etc/postgresql/*/main/pg_hba.conf
```

### Issue: "Directory doesn't exist"

```bash
# Check what version is actually installed
apt list --installed | grep postgresql

# Check all PostgreSQL directories
ls -la /etc/postgresql/

# Use the correct version number
sudo nano /etc/postgresql/[YOUR_VERSION]/main/pg_hba.conf
```

### Issue: "Connection still fails"

```bash
# 1. Check pg_hba.conf was actually changed
sudo cat /etc/postgresql/*/main/pg_hba.conf | grep -v "^#" | grep -v "^$"

# 2. Restart PostgreSQL
sudo systemctl restart postgresql

# 3. Check PostgreSQL logs
sudo tail -f /var/log/postgresql/postgresql-*-main.log

# 4. Try connecting with password explicitly
psql -U django_user -d django_crm -h localhost -W
```

---

## Complete Fresh Setup Script

If you want to start fresh, here's a complete script:

```bash
#!/bin/bash

echo "🔍 Finding PostgreSQL installation..."

# Find PostgreSQL version
PG_VERSION=$(psql --version 2>/dev/null | grep -oP '\d+' | head -1)

if [ -z "$PG_VERSION" ]; then
    echo "❌ PostgreSQL not found. Installing..."
    sudo apt update
    sudo apt install -y postgresql postgresql-contrib
    PG_VERSION=$(psql --version | grep -oP '\d+' | head -1)
fi

echo "✅ PostgreSQL version: $PG_VERSION"

# Find pg_hba.conf
HBA_FILE="/etc/postgresql/$PG_VERSION/main/pg_hba.conf"

if [ ! -f "$HBA_FILE" ]; then
    echo "❌ pg_hba.conf not found at $HBA_FILE"
    echo "🔍 Searching..."
    HBA_FILE=$(sudo -u postgres psql -t -c "SHOW hba_file;" 2>/dev/null | xargs)
    echo "📍 Found at: $HBA_FILE"
fi

# Backup
echo "💾 Creating backup..."
sudo cp "$HBA_FILE" "${HBA_FILE}.backup.$(date +%Y%m%d_%H%M%S)"

# Configure
echo "⚙️  Configuring pg_hba.conf..."
sudo tee "$HBA_FILE" > /dev/null <<EOF
# PostgreSQL Client Authentication Configuration
# TYPE  DATABASE        USER            ADDRESS                 METHOD

# "local" is for Unix domain socket connections only
local   all             postgres                                peer
local   all             all                                     md5

# IPv4 local connections:
host    all             all             127.0.0.1/32            md5

# IPv6 local connections:
host    all             all             ::1/128                 md5

# Allow replication connections
local   replication     all                                     peer
host    replication     all             127.0.0.1/32            md5
host    replication     all             ::1/128                 md5
EOF

# Restart
echo "🔄 Restarting PostgreSQL..."
sudo systemctl restart postgresql

# Test
echo "✅ Testing connection..."
if sudo -u postgres psql -c "SELECT version();" > /dev/null 2>&1; then
    echo "✅ PostgreSQL is configured and running!"
else
    echo "❌ Something went wrong. Check logs: sudo tail /var/log/postgresql/postgresql-$PG_VERSION-main.log"
fi

echo ""
echo "📋 Next steps:"
echo "   1. Create database: sudo -u postgres psql"
echo "   2. Run: CREATE DATABASE django_crm;"
echo "   3. Run: CREATE USER django_user WITH PASSWORD 'your_password';"
echo "   4. Run: GRANT ALL PRIVILEGES ON DATABASE django_crm TO django_user;"
```

Save as `setup_postgresql.sh` and run:
```bash
chmod +x setup_postgresql.sh
./setup_postgresql.sh
```

---

## Summary

**TL;DR:**

```bash
# 1. Find your PostgreSQL version
psql --version

# 2. Find the config file
sudo -u postgres psql -c "SHOW hba_file;"

# 3. Edit it (use the path from step 2)
sudo nano /etc/postgresql/[VERSION]/main/pg_hba.conf

# 4. Change 'peer' to 'md5' for local connections
# 5. Restart PostgreSQL
sudo systemctl restart postgresql
```

---

Need more help? Let me know your PostgreSQL version and I'll give you exact commands!

