FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends cron postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

COPY . .

RUN chmod 0644 /app/crontab \
	&& cp /app/crontab /etc/cron.d/my-cron \
	&& chmod 0644 /etc/cron.d/my-cron \
	&& touch /var/log/cron.log \
	&& chmod 755 /app/scripts/backup_db.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]