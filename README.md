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
- [Variables d'environnement](#-variables-d-environnement)
- [Troubleshooting](#-troubleshooting)
- [License](#license)

## À propos

One Roll To Rule Them All est une plateforme permettant aux photographes de gérer leur équipement photographique (appareils photo, objectifs) et leurs pellicules photo. L'application fournit une interface intuitive pour tracker et organiser sa collection de matériel, depuis l'achat d'une pellicule jusqu'au scan des photos développées.

## Stack technologique

### Backend
- **Django** - Framework web Python
- **Django REST Framework** - API REST
- **Django REST Framework SimpleJWT** - Authentification par tokens JWT
- **drf-spectacular** - Génération automatique de la documentation API (OpenAPI/Swagger)
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
# Documentation API (Swagger UI): http://localhost:8000/api/schema/swagger-ui/
```

## Structure du projet

```
ORTRTA/
├── backend/                           # Application Django (Port 8000)
│   ├── config/                       # Configuration Django
│   │   ├── settings.py              # Paramètres Django
│   │   ├── urls.py                  # Routage principal
│   │   ├── asgi.py                  # Configuration ASGI
│   │   └── wsgi.py                  # Configuration WSGI
│   │
│   ├── core/                        # App principale
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── admin.py
│   │   ├── tests.py
│   │   └── management/commands/     # Commandes personnalisées
│   │
│   ├── equipment/                   # App gestion du matériel photo
│   │   ├── models.py               # Caméra, Objectif, Monture
│   │   ├── views.py                # Viewsets REST
│   │   ├── serializers.py          # Sérializeurs DRF
│   │   ├── permissions.py          # Contrôle d'accès
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── rolls/                       # App gestion des pellicules
│   │   ├── models.py               # Pellicule, Photo (URLPhoto)
│   │   ├── views.py                # Viewsets REST
│   │   ├── serializers.py          # Sérializeurs DRF
│   │   ├── permissions.py          # Contrôle d'accès
│   │   ├── tests.py
│   │   └── migrations/
│   │
│   ├── users/                       # App gestion des utilisateur·ices
│   │   ├── models.py               # Modèle utilisateur personnalisé
│   │   ├── views.py                # Auth, profil, export RGPD
│   │   ├── serializers.py          # Sérializeurs DRF
│   │   ├── signals.py              # Signaux Django
│   │   ├── tests.py
│   │   ├── tests_unit.py           # Tests unitaires supplémentaires
│   │   └── migrations/
│   │
│   ├── logs/                        # Fichiers de logs applicatifs (gitignore)
│   ├── scripts/                     # Scripts utilitaires
│   │   └── backup_db.sh           # Sauvegarde base de données
│   │
│   ├── schema.yaml                  # Export du schéma OpenAPI (YAML)
│   ├── schema.json                  # Export du schéma OpenAPI (JSON)
│   ├── db.sqlite3                   # Base SQLite (développement)
│   ├── manage.py                    # Gestionnaire Django
│   ├── requirements.txt             # Dépendances Python
│   ├── requirements-dev.txt         # Dépendances développement
│   ├── crontab                      # Configuration Cron
│   ├── Dockerfile                   # Image Docker backend
│   └── data.json                    # Données initiales (fixtures)
│
├── frontend/                        # Application Vue 3 (Port 5173)
│   ├── src/
│   │   ├── components/             # Composants Vue réutilisables
│   │   │   ├── BaseButton.vue
│   │   │   ├── EquipmentForm.vue
│   │   │   ├── Footer.vue
│   │   │   └── ...
│   │   ├── views/                  # Pages/vues
│   │   ├── stores/                 # State management (Pinia)
│   │   ├── router/                 # Configuration des routes
│   │   ├── api/                    # Clients API (Axios)
│   │   ├── assets/                 # Images, logos statiques
│   │   ├── App.vue                 # Composant racine
│   │   ├── main.js                 # Point d'entrée
│   │   └── style.css               # Styles globaux
│   │
│   ├── public/                      # Actifs publics statiques
│   ├── package.json                 # Dépendances Node.js
│   ├── vite.config.js              # Configuration Vite
│   ├── tailwind.config.js          # Configuration Tailwind CSS
│   ├── eslint.config.js            # Configuration ESLint
│   ├── jsconfig.json               # Config JS (alias, etc.)
│   ├── index.html                  # HTML principal
│   └── Dockerfile                  # Image Docker frontend
│
├── backups/                         # Sauvegardes de base de données
│   └── backup_*.sql                # Fichiers de sauvegarde
│
├── docker-compose.yml              # Orchestration multi-conteneur
├── .env                            # Variables d'environnement
├── .env.example                    # Template variables (optionnel)
├── PrivacyPolicy.md               # Politique de confidentialité
└── README.md                       # Ce fichier
```

### Modèles de données

#### Equipment (Matériel photo)
- **Camera** : Appareil photo avec monture, présence de lentille fixe
- **Lens** : Objectif avec focales min/max, ouverture
- **Mount** : Type de monture (Canon EF, Nikon F, Sony E, etc.)

#### Rolls (Pellicules)
- **Roll** : Pellicule avec statut (draft, in_progress, developed, archived), ISO, type de film
- **URLPhoto** : URLs de stockage de photos associées à une pellicule

#### Users (Utilisateur·ices)
- **CustomUser** : Utilisateur avec email unique, authentification JWT

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
- ✅ Restrictions de modification/suppression selon le statut (ex : une pellicule scannée ne peut plus être supprimée)
- ✅ Afficher des stockages photo via URL
- ✅ Générer des codes QR pour les pellicules
- ✅ Pagination des résultats
- ✅ Filtrage, recherche et tri des pellicules
- ✅ Statistiques globales (répartition par statut, ISO moyen, répartition par type de film)

### Gestion des utilisateur·ices
- ✅ Système d'authentification
- ✅ Profils utilisateur·ices
- ✅ Modification du mot de passe
- ✅ Export des données personnelles (conformité RGPD)
- ✅ Suppression de compte
- ✅ Permissions personnalisées (chaque utilisateurice accède uniquement à ses propres données)

### Qualité & suivi technique
- ✅ Logging applicatif (actions utilisateurices, erreurs, règles métier) avec rotation des fichiers
- ✅ Documentation API générée automatiquement (OpenAPI / Swagger)

## API

L'API est une API REST accessible à `/api/` sur le backend. Elle est protégée par authentification **JWT** (sauf les endpoints d'inscription, de connexion et de documentation).

### Documentation intéractive
La documentation complète de l'API est générée automatiquement avec **drf-spectacular** et accessible via :
- **Swagger UI** (interface interactive pour tester les endpoints) : http://localhost:8000/api/schema/swagger-ui/
- **ReDoc** (documentation en lecture, plus claire pour une présentation) : http://localhost:8000/api/schema/redoc/  (à faire)
- **Schéma OpenAPI brut** (JSON/YAML, exportable) : http://localhost:8000/api/schema/

Des exports statiques du schéma (schema.yaml et schema.json) sont également disponibles dans le dossier backend/ .

### Endpoints principaux
#### Authentification
- `POST /api/register/` - Créer un compte
- `POST /api/login/` - Se connecter (retourne les tokens JWT)
- `POST /api/token/refresh/` - Rafraîchir le token d'accès

#### Utilisateur·ices
- `GET /api/me` - Récupérer son profil
- `DELETE /api/me` - Supprimer son compte
- `PUT /api/change-password/` - Changer son mot de passe
- `GET /api/me/export/` - Exporter ses données personnelles (RGPD)

#### Equipement
- `GET/POST /api/cameras/` - Gestion des appareils photo
- `GET/POST /api/lenses/` - Gestion des objectifs
- `GET /api/mounts/` - Liste des montures disponibles

#### Pellicules & URL
- `GET/POST /api/rolls/` - Gestion des pellicules (avec pagination, filtres, recherche, tri)
- `GET /api/rolls/{slug}/qr/` - Générer le QR code d'une pellicule
- `GET/POST /api/photos` - Gestion des URL de stockage des photos associées aux pellicules

#### Statistiques
- `GET /api/stats/` - Statistiques globales de l'utilisateur·ice connecté·e

## Développement

### Structure des apps Django

Chaque app Django suit une architecture classique avec permissions personnalisées :

```
app/
├── models.py           # Modèles de données
├── serializers.py      # Sérializeurs DRF (pour l'API REST)
├── views.py            # Viewsets et actions API
├── permissions.py      # Contrôle d'accès personnalisé (ex: IsOwner)
├── admin.py            # Configuration du panneau admin Django
├── apps.py             # Configuration de l'app
├── tests.py            # Tests du modèle
├── migrations/         # Migrations de schéma
└── management/commands/  # (core app uniquement) Commandes personnalisées
```

### Backend

#### 1. Configuration initiale

```bash
# Créez un environnement virtuel
python -m venv venv
source venv/Scripts/activate  # Windows: venv\Scripts\activate

# Installez les dépendances
cd backend
pip install -r requirements.txt
```

#### 2. Migrations & base de données

```bash
# Créer les migrations pour les modifications des modèles
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Créer un superuser (administrateur)
python manage.py createsuperuser
```

#### 3. Charger les données initiales (optionnel)

```bash
# Si un fichier data.json existe (fixtures)
python manage.py loaddata data.json
```

#### 4. Lancer le serveur

```bash
# Développement
python manage.py runserver

# Accès : http://localhost:8000
```

#### 5. Tests

```bash
# Lancer tous les tests
python manage.py test

# Tester une app spécifique
python manage.py test users
python manage.py test equipment
python manage.py test rolls

# Avec verbosité améliorée
python manage.py test --verbosity=2

# Tests de couverture (si coverage est installé)
coverage run --source='.' manage.py test
coverage report
coverage html  # Génère un rapport HTML
```

#### 6. Documentation API

```bash
# Régénérer le schéma OpenAPI (Swagger)
python manage.py spectacular --file schema.yaml

# En JSON
python manage.py spectacular --file schema.json --format openapi-json

# Les schémas sont ensuite accessibles à :
# - Swagger UI: http://localhost:8000/api/schema/swagger-ui/
# - ReDoc: http://localhost:8000/api/schema/redoc/
# - Schéma brut: http://localhost:8000/api/schema/
```

#### 7. Accès à l'admin Django

```
http://localhost:8000/admin
# Connectez-vous avec le superuser créé
```

#### 8. Shell Python Django

```bash
# Accédez au shell interactif
python manage.py shell

# Exemples d'utilisation :
from django.contrib.auth import get_user_model
User = get_user_model()
users = User.objects.all()
```

### Frontend

#### 1. Configuration initiale

```bash
cd frontend
npm install
```

#### 2. Développement (Vite dev server)

```bash
npm run dev

# Accès : http://localhost:5173
# Hot reload automatique
```

#### 3. Linting & Formatting

```bash
# Vérifier les erreurs ESLint
npm run lint

# Formater le code (si formatter configuré)
npm run format
```

#### 4. Build pour production

```bash
# Compiler le bundle optimisé
npm run build

# Le bundle est généré dans le dossier dist/
```

#### 5. Prévisualiser la build

```bash
npm run preview

# Accès : http://localhost:4173
# Permet de vérifier avant le déploiement
```

### Workflow de développement complet

#### 1. **Démarrage local (sans Docker)**

Terminal 1 - Backend :
```bash
cd backend
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Terminal 2 - Frontend :
```bash
cd frontend
npm install
npm run dev
```

Accès :
- Frontend : http://localhost:5173
- Backend : http://localhost:8000
- Admin : http://localhost:8000/admin
- API Docs : http://localhost:8000/api/schema/swagger-ui/

#### 2. **Avec Docker Compose**

```bash
docker-compose up

# Dans un autre terminal, créer un superuser :
docker-compose exec backend python manage.py createsuperuser
```

#### 3. **Ajouter une nouvelle fonctionnalité**

Exemple : Ajouter un champ à un modèle

```bash
# 1. Modifiez le modèle dans models.py
# 2. Créez une migration
python manage.py makemigrations

# 3. Appliquez la migration
python manage.py migrate

# 4. Mettez à jour le sérializeur (serializers.py)
# 5. La nouvelle migration est ensuite appliquée en production
```

### Commandes Docker utiles

```bash
# Voir les logs en temps réel
docker-compose logs -f backend
docker-compose logs -f frontend

# Exécuter une commande Django
docker-compose exec backend python manage.py shell

# Redémarrer un service
docker-compose restart backend

# Arrêter sans supprimer les données
docker-compose stop

# Arrêter et supprimer les conteneurs
docker-compose down

# Supprimer tout (containers + volumes = perte de données)
docker-compose down -v

# Reconstruire les images (après modification de requirements.txt)
docker-compose build --no-cache
```

### Variables d'environnement (Backend)

```python
# settings.py utilise :
DEBUG                   # Mode debug Django
SECRET_KEY             # Clé secrète pour sessions et CSRF
ALLOWED_HOSTS          # Hôtes autorisés
POSTGRES_DB            # Nom base de données
POSTGRES_USER          # Utilisateur PostgreSQL
POSTGRES_PASSWORD      # Mot de passe PostgreSQL
POSTGRES_HOST          # Host PostgreSQL (db en Docker)
POSTGRES_PORT          # Port PostgreSQL
```

## Variables d'environnement

Créez un fichier `.env` à la racine du projet avec les variables suivantes :

```env
# === Django Settings ===
DEBUG=False                           # Mode debug (True en développement)
SECRET_KEY=your-secret-key-here       # Clé secrète pour Django (générer une nouvelle pour production)
ALLOWED_HOSTS=localhost,127.0.0.1     # Hôtes autorisés (ajouter votre domaine en production)

# === Database PostgreSQL ===
POSTGRES_DB=ortrta                    # Nom de la base de données
POSTGRES_USER=ortrta_user             # Utilisateur PostgreSQL
POSTGRES_PASSWORD=your-secure-password # Mot de passe (changer en production)
POSTGRES_HOST=db                      # Host (db en Docker, localhost en développement local)
POSTGRES_PORT=5432                    # Port PostgreSQL

# === Frontend ===
VITE_API_URL=http://localhost:8000/api # URL de l'API pour la frontend

# === Optionnel : Email (pour notifications) ===
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
```

### Pour générer une SECRET_KEY sécurisée :

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Ou en ligne de commande :
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## Authentification & Sécurité

### JWT (JSON Web Token)

L'API utilise **JWT** pour l'authentification stateless :

1. **Obtenir les tokens** :
```bash
curl -X POST http://localhost:8000/api/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Réponse :
# {
#   "access": "eyJ0eXAiOiJKV1QiLCJhbGc.EXEMPLE.token",
#   "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc.EXEMPLE.token"
# }
```

2. **Utiliser le token d'accès** :
```bash
curl http://localhost:8000/api/me/ \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGc.EXEMPLE.token"
```

3. **Rafraîchir le token** (le token d'accès expire après ~5 min) :
```bash
curl -X POST http://localhost:8000/api/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh":"eyJ0eXAiOiJKV1QiLCJhbGc.EXEMPLE.token"}'
```

### Permissions & Contrôle d'accès

- Chaque utilisateur·ice n'accède qu'à **ses propres données**
- Les permissions sont vérifiées au niveau des viewsets (Django REST Framework)
- Classe `IsOwner` personnalisée pour sécuriser l'accès

### RGPD

- **Export des données** : `/api/me/export/` - Télécharge toutes les données personnelles en JSON
- **Suppression de compte** : `/api/me` (DELETE) - Supprime le compte et ses données associées

## Scripts utilitaires

### Sauvegarde de base de données

```bash
# Linux/Mac
bash backend/scripts/backup_db.sh

# Windows (PowerShell ou WSL)
bash backend/scripts/backup_db.sh
```

Les sauvegardes sont stockées dans le dossier `backups/`.

### Tâches Cron

Des tâches automatisées peuvent être configurées via :
- `backend/crontab` : Configuration des jobs cron
- Django Celery Beat (si configuré pour les tâches asynchrones)

### Charger/Exporter des fixtures

```bash
# Exporter des données (fixture)
python manage.py dumpdata > data.json

# Charger des données
python manage.py loaddata data.json

# Exporter une app spécifique
python manage.py dumpdata equipment > equipment.json
```

## Troubleshooting

### Les conteneurs ne démarrent pas

```bash
# Reconstruisez les images
docker-compose build --no-cache
docker-compose up

# Vérifiez les logs
docker-compose logs backend
docker-compose logs frontend
```

### Erreurs de migration

```bash
# Réappliquer les migrations
docker-compose exec backend python manage.py migrate

# Si une migration est bloquée, réinitialisez ( Attention ! supprime les données )
docker-compose exec backend python manage.py migrate zero
docker-compose exec backend python manage.py migrate
```

### Port déjà utilisé

```bash
# Linux/Mac : Trouvez le processus
lsof -i :8000
lsof -i :5173

# Windows : Trouvez le processus
netstat -ano | findstr :8000
# Puis tuez-le : taskkill /PID <PID> /F

# Ou modifiez les ports dans docker-compose.yml
```

### Problèmes de connexion à la base de données

```bash
# Vérifiez que le conteneur PostgreSQL est actif
docker-compose ps

# Redémarrez le service
docker-compose restart db

# Vérifiez les variables .env (POSTGRES_HOST, POSTGRES_PASSWORD, etc.)
```

### Authentification JWT échouée

```bash
# Assurez-vous que :
# 1. La SECRET_KEY est définie dans .env
# 2. Le token n'a pas expiré (créez un nouveau token)
# 3. Le header Authorization est bien formaté : "Bearer <token>"

# Vérifiez le token décrypté (tools en ligne)
# https://jwt.io/
```

### Erreur 404 sur les endpoints API

```bash
# Vérifiez que l'URL de l'API est correcte
# API base : http://localhost:8000/api/

# Consultez la documentation interactive :
# http://localhost:8000/api/schema/swagger-ui/
```

### Frontend ne peut pas accéder à l'API

```bash
# Vérifiez dans .env :
# VITE_API_URL=http://localhost:8000/api

# Vérifiez dans frontend/src/api/axios.js :
# que baseURL utilise VITE_API_URL

# Vérifiez la configuration CORS du backend (settings.py)
```

## Contribution

Pour contribuer au projet :

1. Créez une branche pour votre feature :
```bash
git checkout -b feature/ma-feature
```

2. Commitez vos changements avec un message clair :
```bash
git commit -am "Ajoute nouvelle fonctionnalité"
```

3. Poussez vers la branche :
```bash
git push origin feature/ma-feature
```

4. Ouvrez une Pull Request

### Guide de style

- **Backend** : Suivre [PEP 8](https://pep8.org/) (Python)
- **Frontend** : Suivre [Vue Style Guide](https://vuejs.org/guide/scaling-up/sfc.html)
- **Commits** : Messages en français, descriptifs et concis

## Ressources & Documentation

- **[Django Documentation](https://docs.djangoproject.com/)** - Framework backend
- **[Django REST Framework](https://www.django-rest-framework.org/)** - Construction API REST
- **[drf-spectacular](https://drf-spectacular.readthedocs.io/)** - Génération OpenAPI/Swagger
- **[Vue 3 Documentation](https://vuejs.org/)** - Framework frontend
- **[Vite Documentation](https://vitejs.dev/)** - Build tool et dev server
- **[Pinia Documentation](https://pinia.vuejs.org/)** - State management Vue
- **[Tailwind CSS](https://tailwindcss.com/)** - Utility-first CSS framework
- **[Docker Documentation](https://docs.docker.com/)** - Conteneurisation
- **[PostgreSQL Documentation](https://www.postgresql.org/docs/)** - Base de données


## Support & Signaler un bug

Si vous trouvez un bug ou avez une question :
1. Consultez d'abord les **[Issues](https://github.com/user/repo/issues)**
2. Si non résolu, ouvrez une nouvelle **[Issue](https://github.com/user/repo/issues/new)** avec :
   - Description claire du problème
   - Étapes pour reproduire
   - Stack trace si applicable
   - Environnement (OS, navigateur, version Docker, etc.)

## License

© 2026 Pamela Robinet Duverger

Ce projet est développé avec amour pour les photographes.

---

**Dernière mise à jour** : Juillet 2026  
**Version** : 1.0.0
