#!/bin/sh

set -eu

DATE=$(date +"%Y-%m-%d_%H-%M-%S")
BACKUP_DIR=/backups

DB_HOST_VALUE="${POSTGRES_HOST:-${DB_HOST:-db}}"
DB_NAME_VALUE="${POSTGRES_DB:-${DB_NAME:-}}"
DB_USER_VALUE="${POSTGRES_USER:-${DB_USER:-}}"
DB_PASSWORD_VALUE="${POSTGRES_PASSWORD:-${DB_PASSWORD:-}}"

if [ -z "$DB_NAME_VALUE" ] || [ -z "$DB_USER_VALUE" ] || [ -z "$DB_PASSWORD_VALUE" ]; then
	echo "Missing DB credentials. Define POSTGRES_* or DB_* variables." >&2
	exit 1
fi

mkdir -p "$BACKUP_DIR"

export PGPASSWORD="$DB_PASSWORD_VALUE"
pg_dump -h "$DB_HOST_VALUE" -U "$DB_USER_VALUE" "$DB_NAME_VALUE" > "$BACKUP_DIR/backup_$DATE.sql"

find "$BACKUP_DIR" -type f -mtime +7 -delete # pour ne garder que les 7 derniers jours de backup

echo "Backup done: backup_$DATE.sql"