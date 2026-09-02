# DEPLOYMENT.md — One Roll To Rule Them All (ORTRTA)

Procédure de déploiement en production sur VPS Scaleway.

> Ce document décrit **le déroulé opérationnel** du déploiement.

---

## 1. Prérequis

Avant de commencer, s'assurer d'avoir :

- [ ] Un accès SSH au VPS, via une clé dédiée (ex. `id_ed25519_scaleway`)
- [ ] Le nom de domaine acheté et accessible dans son espace de gestion DNS (ex. OVH)
- [ ] La liste des variables nécessaires au fichier `.env` de production (voir section 4)
- [ ] Git installé en local, avec accès en lecture au dépôt GitHub du projet

---

## 2. Provisionnement du serveur

### 2.1 Création de l'instance

- Hébergeur : Scaleway
- Type d'instance : DEV1-S (2 vCPU, 2 Go RAM, 10 Go stockage, IPv4 + IPv6)
- OS : Ubuntu 24.04 LTS
- Une paire de clés SSH dédiée au projet est ajoutée à la création de l'instance.

### 2.2 Connexion et installation de Docker

Depuis le PC local (Windows / PowerShell) :

```powershell
ssh -i $env:USERPROFILE\.ssh\id_ed25519_scaleway root@163.172.14.39
```

Toutes les commandes qui suivent, dans le reste de ce document,
s'exécutent **sur le serveur**, en Bash, une fois connectée en SSH.

Mise à jour du système et installation de Docker via le script officiel :

```bash
apt update && apt upgrade -y

curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

docker --version
docker compose version
```

### 2.3 Clonage du dépôt

```bash
cd /opt
git clone https://github.com/Pampamlela/ORTRTA.git
cd ORTRTA
```

---

## 3. Configuration DNS

Dans la zone DNS du domaine (ex. manager OVH) :

| Type  | Sous-domaine | Cible                          |
|-------|--------------|---------------------------------|
| A     | `@`          | IP publique du VPS Scaleway    |
| CNAME | `www`        | `oneroll.fr.` (point final inclus) |

> Un enregistrement `www` ne peut pas cumuler un CNAME et un autre type
> (A, TXT...). Supprimer tout enregistrement existant pour `www` avant de
> créer le CNAME.

Vérifier la propagation depuis le serveur :

```bash
dig oneroll.fr
dig www.oneroll.fr
```

→ Les deux commandes doivent renvoyer l'IP du VPS dans la section `ANSWER`.
La propagation peut prendre de quelques minutes à plusieurs heures.

---

## 4. Configuration des fichiers de production

### 4.1 Fichier `.env`

À la racine de `/opt/ORTRTA`, créer le fichier `.env` et le sécuriser :

```bash
nano .env
chmod 600 .env
```

Variables à renseigner (valeurs réelles, jamais de placeholder laissé tel quel) :

```env
# Django
SECRET_KEY=<clé secrète Django générée pour la prod>
DEBUG=False
ALLOWED_HOSTS=oneroll.fr,www.oneroll.fr
CORS_ALLOWED_ORIGINS=https://oneroll.fr,https://www.oneroll.fr
FRONTEND_URL=https://oneroll.fr

# Base de données
# DB_PASSWORD doit être IDENTIQUE à POSTGRES_PASSWORD dans docker-compose.prod.yml
DB_NAME=ortrta
DB_USER=ortrta_user
DB_PASSWORD=<mot de passe fort>
DB_HOST=db
DB_PORT=5432

# Email
EMAIL_HOST_USER=<adresse email d'envoi>
EMAIL_HOST_PASSWORD=<mot de passe applicatif>
```

### 4.2 Cohérence avec `docker-compose.prod.yml`

Vérifier que les valeurs `POSTGRES_DB` / `POSTGRES_USER` / `POSTGRES_PASSWORD`
du service `db` dans `docker-compose.prod.yml` correspondent exactement à
`DB_NAME` / `DB_USER` / `DB_PASSWORD` du `.env`.

### 4.3 Fichier `Caddyfile`

Vérifier que le bloc d'en-tête liste bien les deux noms de domaine :

```
oneroll.fr, www.oneroll.fr {
    handle /api/* {
        reverse_proxy backend:8000
    }
    handle {
        reverse_proxy frontend:80
    }
}
```

---

## 5. Build et démarrage des conteneurs

```bash
docker compose -f docker-compose.prod.yml up -d --build
```

Vérifier que tous les services sont bien démarrés :

```bash
docker compose -f docker-compose.prod.yml ps
```

→ Tous les conteneurs doivent afficher le statut `Up`.

Consulter les logs en cas de doute sur un service en particulier :

```bash
docker compose -f docker-compose.prod.yml logs backend
docker compose -f docker-compose.prod.yml logs caddy
docker compose -f docker-compose.prod.yml logs cron
```

---

## 6. Initialisation de la base de données

Appliquer les migrations Django :

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

Créer un compte superuser (accès à l'admin Django) :

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py createsuperuser
```

---

## 7. Vérification post-déploiement

### 7.1 Certificat HTTPS

Vérifier dans les logs de Caddy l'obtention du certificat Let's Encrypt :

```bash
docker compose -f docker-compose.prod.yml logs caddy | grep "certificate obtained successfully"
```

→ Une ligne doit apparaître pour `oneroll.fr` et une pour `www.oneroll.fr`.

### 7.2 Réponses HTTP

```bash
curl -I https://oneroll.fr/
curl -I https://www.oneroll.fr/
curl -I https://oneroll.fr/login
```

→ Chaque commande doit renvoyer `HTTP/2 200`.

### 7.3 Checklist finale

- [ ] `dig oneroll.fr` et `dig www.oneroll.fr` renvoient l'IP du VPS
- [ ] Tous les conteneurs sont `Up` (`docker compose ps`)
- [ ] Certificat HTTPS obtenu pour les deux domaines
- [ ] `curl -I` renvoie `200` sur `/` et sur au moins une route protégée
- [ ] Les migrations sont toutes appliquées sans erreur
- [ ] Un compte peut être créé depuis l'interface (`/register`)
- [ ] La connexion fonctionne (`/login`) et redirige vers l'application
- [ ] Un appareil photo et une pellicule peuvent être créés depuis l'interface
- [ ] Le superuser peut accéder à `/admin`