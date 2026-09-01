#!/bin/sh
set -e

# permissions sur le script de backup s'il existe
if [ -f /app/scripts/backup_db.sh ]; then
    chmod 755 /app/scripts/backup_db.sh
fi

# mise en place du crontab
if [ -f /app/crontab ]; then
    chmod 0644 /app/crontab
    cp /app/crontab /etc/cron.d/my-cron
    chown root:root /etc/cron.d/my-cron
    chmod 0644 /etc/cron.d/my-cron
fi

# fichier de log pour cron
# seul le demon cron (root) écrit ici 
touch /var/log/cron.log
chown root:root /var/log/cron.log
chmod 0644 /var/log/cron.log