# base commmune : dépendances système et python
FROM python:3.12-slim AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

RUN python -m pip install --no-cache-dir --upgrade pip==26.0

# cron : nécessaire pour le service "cron"
# postgresql-client : nécessaire pour le script de backup (pg_dump)
RUN apt-get update && apt-get install -y --no-install-recommends cron postgresql-client \
	&& rm -rf /var/lib/apt/lists/*

COPY requirements.txt requirements-dev.txt ./

# stage de transition : mise en place du cron
# isolé ici pour ne copier que le strict nécessaire et préserver le cache Docker sur les étapes de "base"
FROM base AS base-cron

COPY crontab ./crontab
COPY scripts/setup-cron.sh ./scripts/setup-cron.sh
RUN chmod +x ./scripts/setup-cron.sh && ./scripts/setup-cron.sh

# étape développement
FROM base-cron AS dev

RUN pip install --no-cache-dir -r requirements-dev.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

# étape production : API (Gunicorn) tourne en utilisateur non-root
FROM base-cron AS prod

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Le dossier logs/ n'est pas versionné (.gitignore) donc absent après le COPY. .
# On le crée nous-mêmes et on le donne à monuser AVANT de basculer dessus,
# sinon Gunicorn (qui tournera en tant que monuser) ne pourra pas y écrire.
RUN useradd -m monuser \
	&& mkdir -p /app/logs \
	&& chown -R monuser:monuser /app/logs

USER monuser

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "config.wsgi:application"]

# production : cron
# Doit rester root : crond refuse d'exécuter les jobs définis dans /etc/cron.d/
# si le fichier n'appartient pas à root, et ne peut pas gérer les tâches système
# correctement s'il est lui-même lancé par un utilisateur non-privilégié
FROM base-cron AS cron

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["cron", "-f"]