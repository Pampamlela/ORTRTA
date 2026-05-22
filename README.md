# One Roll To Rule Them All (ORTRTA)

Une application complète de gestion de matériel photographique et de pellicules photo.

## Table des matières

- [À propos](#à-propos)
- [Stack technologique](#-stack-technologique)
- [Prérequis](#-prérequis)
- [Installation](#-installation)
- [Démarrage rapide](#-démarrage-rapide)
- [Structure du projet](#-structure-du-projet)
- [Fonctionnalités](#-fonctionnalités)
- [API](#-api)
- [Développement](#-développement)
- [License](#license)

## À propos

ORTRTA est une plateforme permettant aux photographes de gérer leur équipement photographique (appareils photo, objectifs) et leurs pellicules photo. L'application fournit une interface intuitive pour tracker et organiser votre collection de matériel.

## Stack technologique

### Backend
- **Django** - Framework web Python
- **Django REST Framework** - API REST
- **PostgreSQL** - Base de données
- **Gunicorn/Asgiref** - Serveur WSGI/ASGI

### Frontend
- **Vue 3** - Framework JavaScript progressif
- **Vite** - Build tool et dev server
- **Vue Router** - Routage côté client
- **Pinia** - State management
- **Tailwind CSS** - Styling utility-first
- **Axios** - HTTP client

### DevOps
- **Docker** - Conteneurisation
- **Docker Compose** - Orchestration multi-conteneur
- **PostgreSQL** - Base de données en conteneur

## Prérequis

- **Docker** et **Docker Compose** (recommandé)
- Ou alternativement :
  - Python 3.10+
  - Node.js 20.19.0+ ou 22.12.0+
  - PostgreSQL 15+

## Installation

### Option 1 : Avec Docker (Recommandé)

1. Clonez le repository :
```bash
git clone <repository-url>
cd ORTRTA
```

2. Créez un fichier `.env` à la racine du projet :
```bash
cp .env.example .env  # Si le fichier existe
# Sinon créez-le avec les variables nécessaires
```

3. Lancez l'application :
```bash
docker-compose up
```

L'application sera accessible à :
- Backend : `http://localhost:8000`
- Frontend : `http://localhost:5173` (ou `http://localhost` après build)

### Option 2 : Installation manuelle

#### Backend

1. Installez les dépendances Python :
```bash
cd backend
pip install -r requirements.txt
```

2. Migrez la base de données :
```bash
python manage.py migrate
```

3. Créez un superuser (administrateur) :
```bash
python manage.py createsuperuser
```

4. Démarrez le serveur :
```bash
python manage.py runserver
```

#### Frontend

1. Installez les dépendances :
```bash
cd frontend
npm install
```

2. Démarrez le dev server :
```bash
npm run dev
```

## Démarrage rapide

Après installation avec Docker :

```bash
# Démarrez les services
docker-compose up

# Dans un autre terminal, créez un superuser
docker-compose exec backend python manage.py createsuperuser

# Accédez à l'application
# Frontend: http://localhost:5173
# Admin: http://localhost:8000/admin
```

## Structure du projet

```
ORTRTA/
├── backend/                    # Application Django
│   ├── config/                # Configuration Django (settings, urls, wsgi)
│   ├── core/                  # App principale
│   ├── equipment/             # App gestion des appareils et objectifs
│   ├── rolls/                 # App gestion des pellicules
│   ├── users/                 # App gestion des utilisateurs
│   ├── manage.py
│   ├── requirements.txt        # Dépendances Python
│   └── Dockerfile
│
├── frontend/                   # Application Vue 3
│   ├── src/
│   │   ├── components/        # Composants Vue
│   │   ├── views/             # Pages
│   │   ├── stores/            # State (Pinia)
│   │   ├── router/            # Configuration des routes
│   │   └── api/               # Appels API
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── docker-compose.yml          # Configuration Docker Compose
├── .env                        # Variables d'environnement
└── README.md                   # Ce fichier
```

## Fonctionnalités

### Gestion du matériel
- ✅ Ajouter/modifier/supprimer des appareils photo
- ✅ Gérer les objectifs et leurs montures
- ✅ Tracker les appareils avec lentille fixe
- ✅ Organiser votre équipement

### Gestion des pellicules
- ✅ Créer et tracker des pellicules photo
- ✅ Assigner un équipement aux pellicules
- ✅ Gérer le statut des pellicules (en cours, développée, archivée)
- ✅ Associer des photos via URL
- ✅ Générer des codes QR pour les pellicules

### Gestion des utilisateurs
- ✅ Système d'authentification
- ✅ Profils utilisateurs
- ✅ Permissions personnalisées

## API

L'API est une API REST accessible à `/api/` sur le backend.

### Endpoints principaux

- `GET/POST /api/equipment/cameras/` - Gestion des appareils photo
- `GET/POST /api/equipment/lenses/` - Gestion des objectifs
- `GET/POST /api/rolls/` - Gestion des pellicules
- `GET/POST /api/users/` - Gestion des utilisateurs

### Documentation API

Pour accéder à la documentation interactive de l'API (si disponible) :
- `http://localhost:8000/api/docs` (via drf-spectacular)

## Développement

### Backend

1. Créer une migration :
```bash
python manage.py makemigrations
```

2. Appliquer les migrations :
```bash
python manage.py migrate
```

3. Lancer les tests :
```bash
python manage.py test
```

4. Accéder à l'admin Django :
```
http://localhost:8000/admin
```

### Frontend

1. Linter et formatter le code :
```bash
npm run lint
npm run format
```

2. Builder pour la production :
```bash
npm run build
```

3. Prévisualiser la build :
```bash
npm run preview
```

### Scripts utiles

- **Backup de la base de données** :
```bash
bash backend/scripts/backup_db.sh
```

- **Cron jobs** : Des tâches automatisées peuvent être configurées via le service `cron` dans Docker Compose.

## Commandes utiles avec Docker

```bash
# Voir les logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Exécuter des commandes Django
docker-compose exec backend python manage.py [command]

# Accéder au shell Python Django
docker-compose exec backend python manage.py shell

# Redémarrer un service
docker-compose restart backend

# Arrêter les services
docker-compose down

# Supprimer tous les volumes (données)
docker-compose down -v
```

## Variables d'environnement

Créez un fichier `.env` à la racine du projet :

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
POSTGRES_DB=ortrta
POSTGRES_USER=ortrta_user
POSTGRES_PASSWORD=your-secure-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

# Frontend
VITE_API_URL=http://localhost:8000/api
```

## Troubleshooting

### Les conteneurs ne démarrent pas
```bash
# Reconstruisez les images
docker-compose build --no-cache
docker-compose up
```

### Erreurs de migration
```bash
# Réinitialisez les migrations (attention : cela supprime les données)
docker-compose exec backend python manage.py migrate zero
docker-compose exec backend python manage.py migrate
```

### Port déjà utilisé
```bash
# Modifiez les ports dans docker-compose.yml
# Ou tuez le processus utilisant le port :
# Linux/Mac: lsof -i :8000
# Windows: netstat -ano | findstr :8000
```

## Développement

Pamela Robinet Duverger

---

**Besoin d'aide ?** Consultez les documentations officielles :
- [Django Documentation](https://docs.djangoproject.com/)
- [Vue 3 Documentation](https://vuejs.org/)
- [Docker Documentation](https://docs.docker.com/)
