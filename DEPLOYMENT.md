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
- [ ] Un compte [Resend](https://resend.com) créé, avec une clé API générée (voir section 3.1)

---

## 2. Provisionnement du serveur

### 2.1 Création de l'instance

- Hébergeur : Scaleway
- Type d'instance : DEV1-S (2 vCPU, 2 Go RAM, 10 Go stockage, IPv4 + IPv6)
- OS : Ubuntu 24.04 LTS
- Une paire de clés SSH dédiée au projet est ajoutée à la création de l'instance.

> **Port SMTP sortant bloqué par défaut.** Scaleway (comme la plupart des
> hébergeurs cloud bon marché) bloque le trafic SMTP sortant (port 587/25)
> sur ce type d'instance, pour lutter contre le spam. L'envoi d'e-mails
> transactionnels (réinitialisation de mot de passe) passe donc par
> **Resend**, via une API HTTPS (port 443, jamais bloqué) — voir section 3.1
> et 4.1.

### 2.2 Connexion et installation de Docker

Depuis le PC local (Windows / PowerShell) :

```powershell
ssh -i $env:USERPROFILE\.ssh\id_ed25519_scaleway root@<IP>
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

### 3.1 Enregistrements de base (routage du site)

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

### 3.2 Enregistrements Resend (envoi d'e-mails)

Depuis le dashboard Resend, section **Domains → Add Domain**, ajouter
`oneroll.fr` puis reporter les enregistrements fournis dans la zone DNS OVH :

| Type | Nom (exemple)         | Contenu (fourni par Resend)     | Rôle                          |
|------|------------------------|----------------------------------|-------------------------------|
| TXT  | `resend._domainkey`    | `p=MIGfMA0G...` (sans le `p=` initial dans le champ « Clé publique » du formulaire DKIM d'OVH) | Authentification DKIM |
| CNAME | `rsend`                | `rsend-euX.forge.rmta.net`      | SPF / gestion des bounces     |
| CNAME | `send`                 | `send.forX.rmta.net`            | SPF / gestion des bounces     |

> Sur le formulaire DKIM d'OVH, ne pas coller le préfixe `p=` fourni par
> Resend — seul ce qui suit va dans le champ « Clé publique (base64) ».
> Type de clé : **RSA**. Mode test : **Désactivé** (le domaine sert de la
> vraie production, pas d'un test).
>
> Pour le SPF, les deux lignes `rsend` et `send` sont des **CNAME**, pas des
> enregistrements de type "SPF" à IP — ne pas utiliser l'assistant SPF
> générique d'OVH pour ces deux-là.

Vérifier la propagation du DKIM depuis le serveur :

```bash
dig TXT resend._domainkey.oneroll.fr
```

→ Doit renvoyer la clé publique fournie par Resend dans la section `ANSWER`.

Le domaine passe généralement en statut **"Verified"** sur le dashboard
Resend dans les 15 minutes suivant l'ajout des enregistrements (parfois plus
selon la propagation DNS OVH).

---

## 4. Configuration des fichiers de production

### 4.1 Fichier `.env`

À la racine de `/opt/ORTRTA`, créer le fichier `.env` et le sécuriser :

```bash
nano .env
chmod 600 .env
```

> ⚠️ Ce fichier est créé et édité **directement sur le VPS**, jamais en
> local puis copié — il n'est pas versionné dans Git (`.gitignore`), donc un
> `git pull` ne le mettra jamais à jour. Toute variable ajoutée doit être
> vérifiée sur place avec `grep NOM_VARIABLE .env`.

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

# Email (Resend — voir section 3.2 pour la vérification du domaine)
RESEND_API_KEY=<clé API générée sur le dashboard Resend>
DEFAULT_FROM_EMAIL=noreply@oneroll.fr
```

> L'envoi d'e-mails ne passe plus par un serveur SMTP classique
> (`EMAIL_HOST_USER` / `EMAIL_HOST_PASSWORD`, abandonné) mais par l'API
> HTTPS de Resend via `django-anymail`, pour contourner le blocage du port
> SMTP sortant sur Scaleway (voir encart section 2.1). Tant que
> `DEFAULT_FROM_EMAIL` n'est pas définie, Django utilise la valeur par
> défaut `onboarding@resend.dev` — un domaine de test Resend, à ne pas
> laisser en prod.

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

> **Après toute modification du `.env`**, les conteneurs doivent être
> reconstruits/redémarrés pour prendre en compte les nouvelles valeurs — les
> variables d'environnement sont injectées au démarrage du conteneur, pas
> lues en continu. `docker compose -f docker-compose.prod.yml up -d --build`
> suffit (pas besoin de préciser un service en particulier, sauf pour
> accélérer le redéploiement, ex. `... up -d --build backend`).

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

### 7.3 Vérification de l'envoi d'e-mails (Resend)

D'abord, confirmer que la configuration est bien chargée dans le conteneur :

```bash
docker compose -f docker-compose.prod.yml exec backend python manage.py shell
```

```python
from django.conf import settings
print(settings.EMAIL_BACKEND)   # doit afficher "anymail.backends.resend.EmailBackend"
print(settings.ANYMAIL)         # doit afficher la vraie clé RESEND_API_KEY, pas None
print(settings.DEFAULT_FROM_EMAIL)  # doit afficher noreply@oneroll.fr, pas onboarding@resend.dev
```

> **Ne pas tester l'envoi via `ResetPasswordToken.objects.create(...)`
> dans le shell.** Le signal `reset_password_token_created` n'est déclenché
> que dans la méthode `post()` de la vue HTTP de `django-rest-passwordreset`
> — créer le token directement via l'ORM contourne cette vue et ne déclenche
> jamais l'envoi du mail, donnant un faux sentiment que "rien n'est cassé"
> alors que rien n'a été testé.

Le seul test fiable est de passer par le vrai flow HTTP :

1. Aller sur `https://oneroll.fr/forgot-password`
2. Soumettre une adresse e-mail réelle et accessible
3. Vérifier sur le [dashboard Resend](https://resend.com/emails) (section
   Logs / Emails) qu'un envoi apparaît, avec le statut `Delivered`
4. Vérifier dans la boîte mail reçue que :
   - le lien pointe vers `https://oneroll.fr/reset-password?token=...`
     (pas `localhost:5173`)
   - l'expéditeur est `noreply@oneroll.fr` (pas `onboarding@resend.dev`)
5. Cliquer sur le lien, réinitialiser le mot de passe, et confirmer que la
   connexion fonctionne avec le nouveau mot de passe

### 7.4 Checklist finale

- [ ] `dig oneroll.fr` et `dig www.oneroll.fr` renvoient l'IP du VPS
- [ ] `dig TXT resend._domainkey.oneroll.fr` renvoie la clé DKIM Resend
- [ ] Domaine `oneroll.fr` en statut "Verified" sur le dashboard Resend
- [ ] Tous les conteneurs sont `Up` (`docker compose ps`)
- [ ] Certificat HTTPS obtenu pour les deux domaines
- [ ] `curl -I` renvoie `200` sur `/` et sur au moins une route protégée
- [ ] Les migrations sont toutes appliquées sans erreur
- [ ] Un compte peut être créé depuis l'interface (`/register`)
- [ ] La connexion fonctionne (`/login`) et redirige vers l'application
- [ ] Un appareil photo et une pellicule peuvent être créés depuis l'interface
- [ ] Le superuser peut accéder à `/admin`
- [ ] `RESEND_API_KEY` et `DEFAULT_FROM_EMAIL` confirmées dans le `.env` du
      VPS avec `grep` (pas seulement supposées ajoutées)
- [ ] Un e-mail de réinitialisation de mot de passe envoyé depuis
      `/forgot-password` arrive bien, avec le bon lien et le bon expéditeur
      (voir section 7.3 — test via le vrai formulaire, pas via le shell)