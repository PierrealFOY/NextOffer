# <img src="./frontend/public/favicon.ico" width="40"> NextOffer

NextOffer est une application web qui récupère et affiche des offres d'emploi depuis deux API publiques : **France Travail** et **Remotive**.

Ce projet a été réalisé avec ❤️ par un développeur full-stack passionné d’UX et backend.

### 🤖 Stack Technique

**Frontend :**

- Vue.js (TypeScript)
- TailwindCSS
- Vite
- Pinia
- Shadcn

**Backend :**

- Node.js
- Python + FastAPI
- Pydantic (validation)
- PostgreSQL (base de données)

### 🐋 Environnement & Docker

#### Développement (local)

- Le frontend tourne en mode dev avec `npm run dev` (via Docker ou localement).
- Le backend se lance en mode debug.
- Le fichier `nginx/nginx.local.conf` configure Nginx localement.
- Le fichier `docker-compose.local.yml` orchestre les services pour le dev.

#### Production (VPS)

- Le frontend est buildé (`npm run build`) et servi via Nginx.
- Le backend est déployé en mode production.
- Le fichier `nginx/nginx.vps.conf` configure Nginx pour la prod.
- Le fichier `docker-compose.vps.yml` orchestre les services pour la prod (backend, frontend, db, nginx, adminer).
- Les certificats SSL sont gérés via Certbot (commenté pour l’instant).

&rarr; le site est hebergé sur un VPS via OVH

### 🌁 APIs utilisées

- **France Travail** : API officielle française d’offres d’emploi.
- **Remotive** : API externe d’offres d’emploi internationales.

Ces API sont appelées côté backend pour récupérer, filtrer et exposer les offres au frontend.

### 📟 Commandes Docker principales

- Pour lancer en local :

```bash
    docker-compose -f docker-compose.local.yml up --build
```

- Pour lancer en production (sur VPS) :

```bash
    docker-compose -f docker-compose.vps.yml up --build -d
```

### ☎️ Contact

Pour toute question, suggestion ou collaboration, n’hésitez pas à me contacter :

- LinkedIn : [[lien LinkedIn](https://www.linkedin.com/in/pierre-alexis-foy/)]

- Email : [pierre.alexis.56@gmail.com]

### 🙌 Remerciements

Merci d'avoir consulté NextOffer. Ce projet est une belle aventure entre frontend moderne, backend robuste et intégration d’APIs externes.
