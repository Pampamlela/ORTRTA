# base commmune
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip==26.0

RUN apt-get update && apt-get install -y --no-install-recommends cron postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./

# étape développement
FROM base AS dev

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

RUN chmod 0644 /app/crontab \
	&& cp /app/crontab /etc/cron.d/my-cron \
	&& chmod 0644 /etc/cron.d/my-cron \
	&& touch /var/log/cron.log \
	&& chmod 755 /app/scripts/backup_db.sh

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# étape production
FROM base AS prod

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod 0644 /app/crontab \
	&& cp /app/crontab /etc/cron.d/my-cron \
	&& chmod 0644 /etc/cron.d/my-cron \
	&& touch /var/log/cron.log \
	&& chmod 755 /app/scripts/backup_db.sh

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]