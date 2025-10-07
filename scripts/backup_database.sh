#!/bin/bash

# Database Backup Script for Django CRM
# Usage: ./scripts/backup_database.sh

BACKUP_DIR="/var/backups/django_crm"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="django_crm"

# Create backup directory
mkdir -p $BACKUP_DIR

# Check if using PostgreSQL or SQLite
if [ -f "db.sqlite3" ]; then
    echo "Backing up SQLite database..."
    cp db.sqlite3 "$BACKUP_DIR/db_backup_$DATE.sqlite3"
    gzip "$BACKUP_DIR/db_backup_$DATE.sqlite3"
    echo "SQLite backup completed: $BACKUP_DIR/db_backup_$DATE.sqlite3.gz"
else
    echo "Backing up PostgreSQL database..."
    pg_dump -U postgres -d $DB_NAME -F c -f "$BACKUP_DIR/db_backup_$DATE.dump"
    gzip "$BACKUP_DIR/db_backup_$DATE.dump"
    echo "PostgreSQL backup completed: $BACKUP_DIR/db_backup_$DATE.dump.gz"
fi

# Keep only last 7 days of backups
find $BACKUP_DIR -name "db_backup_*" -mtime +7 -delete

echo "Backup completed successfully!"
echo "Old backups (>7 days) have been removed."

