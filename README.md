
<div align="center">
  
# 🤖 IA Générative - Full Stack Application

[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Angular](https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white)](https://angular.io/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)

**Application web moderne de génération de contenu par Intelligence Artificielle**

[Démo Live](#) • [Documentation](#-documentation-api) • [Installation](#-installation)

</div>

---

## 📋 Table des matières

- [À propos](#-à-propos)
- [Fonctionnalités](#-fonctionnalités)
- [Démo](#-démo)
- [Technologies](#️-technologies)
- [Architecture](#-architecture)
- [Installation](#-installation)
- [Utilisation](#-utilisation)
- [Documentation API](#-documentation-api)
- [Structure du projet](#-structure-du-projet)
- [Roadmap](#-roadmap)
- [Auteur](#-auteur)
- [Licence](#-licence)

---

## 📖 À propos

Ce projet est une **application full-stack** permettant de générer du contenu via l'Intelligence Artificielle :

- 📝 **Texte** : Génération de texte avec LLaMA 3.3 (70B paramètres)
- 🖼️ **Images** : Création d'images avec Stable Diffusion XL
- 🎬 **Vidéos** : Production de vidéos cinématiques avec effets Ken Burns

Le projet démontre une architecture moderne avec **séparation frontend/backend**, **conteneurisation Docker**, et **intégration d'APIs IA**.

---

## ✨ Fonctionnalités

| Fonctionnalité | Description |
|----------------|-------------|
| 📝 **Génération de texte** | Réponses intelligentes via LLaMA 3.3 (Groq API) |
| 🖼️ **Génération d'images** | 7 styles artistiques (photo, art, anime, cinematic...) |
| 🎬 **Génération de vidéos** | Vidéos avec effets Ken Burns, transitions, color grading |
| 🎨 **Interface moderne** | Design glassmorphism, animations fluides, responsive |
| 🐳 **Dockerisé** | Déploiement en une commande |
| 📡 **API REST** | Endpoints documentés avec Swagger UI |

---

## 🎥 Démo

### Interface principale
┌─────────────────────────────────────────────────────────────┐
│ 🤖 IA Générative │
├─────────────────────────────────────────────────────────────┤
│ │
│ Entrez votre prompt : │
│ ┌─────────────────────────────────────────────────────┐ │
│ │ Un chat astronaute sur la lune │ │
│ └─────────────────────────────────────────────────────┘ │
│ │
│ [📝 Texte] [🖼️ Image] [🎬 Vidéo] │
│ │
│ [ 🚀 GÉNÉRER ] │
│ │
└─────────────────────────────────────────────────────────────┘

text


### Exemples de génération

| Type | Prompt | Résultat |
|------|--------|----------|
| 📝 Texte | "Explique Docker en 2 phrases" | Réponse IA complète |
| 🖼️ Image | "A bird flying, cinematic style" | Image HD générée |
| 🎬 Vidéo | "Sunset over mountains" | Vidéo MP4 avec effets |

---

## 🛠️ Technologies

### Backend
| Technologie | Usage |
|-------------|-------|
| ![Python](https://img.shields.io/badge/Python_3.11-3776AB?style=flat-square&logo=python&logoColor=white) | Langage principal |
| ![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white) | Framework API REST |
| ![Groq](https://img.shields.io/badge/Groq_API-FF6B6B?style=flat-square) | LLaMA 3.3 pour le texte |
| ![HuggingFace](https://img.shields.io/badge/HuggingFace-FFD21E?style=flat-square&logo=huggingface&logoColor=black) | Stable Diffusion pour les images |
| ![FFmpeg](https://img.shields.io/badge/FFmpeg-007808?style=flat-square&logo=ffmpeg&logoColor=white) | Traitement vidéo |

### Frontend
| Technologie | Usage |
|-------------|-------|
| ![Angular](https://img.shields.io/badge/Angular_17-DD0031?style=flat-square&logo=angular&logoColor=white) | Framework frontend |
| ![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white) | Langage typé |
| ![SCSS](https://img.shields.io/badge/SCSS-CC6699?style=flat-square&logo=sass&logoColor=white) | Styles avancés |

### DevOps
| Technologie | Usage |
|-------------|-------|
| ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white) | Conteneurisation |
| ![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white) | Serveur web / Reverse proxy |
| ![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white) | Versioning |

---

## 🏗 Architecture
┌─────────────────────────────────────────────────────────────┐
│ ARCHITECTURE │
├─────────────────────────────────────────────────────────────┤
│ │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ │ │ │ │ │ │
│ │ FRONTEND │◄────►│ NGINX │◄────►│ BACKEND │ │
│ │ (Angular) │ │ (Proxy) │ │ (FastAPI) │ │
│ │ │ │ │ │ │ │
│ └─────────────┘ └─────────────┘ └──────┬──────┘ │
│ │ │
│ ┌──────▼──────┐ │
│ │ APIs IA │ │
│ │ Groq / HF │ │
│ └─────────────┘ │
│ │
└─────────────────────────────────────────────────────────────┘

text


### Flux de données
Utilisateur → Frontend (Angular)
↓
Nginx (Proxy)
↓
Backend (FastAPI)
↓
APIs IA (Groq / HuggingFace)
↓
Résultat → Utilisateur

text


---

## 🚀 Installation

### Prérequis

- [Docker Desktop](https://www.docker.com/products/docker-desktop) installé
- Clés API :
  - [Groq API](https://console.groq.com/) (gratuit)
  - [HuggingFace](https://huggingface.co/settings/tokens) (gratuit)

### Installation avec Docker (recommandé)

*bash
# 1. Clone le repository
git clone https://github.com/meddeiaa/projet-ia-generative.git
cd projet-ia-generative

# 2. Crée le fichier .env
cp backend/.env.example backend/.env
# Puis édite backend/.env avec tes clés API

# 3. Lance l'application
docker compose up --build

# 4. Ouvre dans ton navigateur
# Frontend : http://localhost:3000
# Backend  : http://localhost:8000
Installation manuelle (développement)
<details> <summary>Cliquez pour voir les instructions</summary>
Backend
Bash

cd backend
python -m venv venv
.\venv\Scripts\Activate  # Windows
source venv/bin/activate # Mac/Linux
pip install -r requirements.txt
python main.py
Frontend
Bash

cd frontend
npm install
ng serve
</details>
📖 Utilisation
1. Génération de texte
text

1. Ouvre http://localhost:3000
2. Entre ton prompt : "Explique-moi l'IA en termes simples"
3. Clique sur "📝 Texte"
4. Clique "GÉNÉRER"
5. Lis la réponse générée !
2. Génération d'image
text

1. Entre ton prompt : "A futuristic city at night"
2. Sélectionne un style (ex: "cinematic")
3. Clique sur "🖼️ Image"
4. Clique "GÉNÉRER"
5. Attends ~10 secondes
6. Admire ton image !
3. Génération de vidéo
text

1. Entre ton prompt : "Ocean waves on a beach"
2. Clique sur "🎬 Vidéo"
3. Clique "GÉNÉRER"
4. Attends ~60 secondes
5. Télécharge ta vidéo MP4 !
📡 Documentation API
Endpoints disponibles
Méthode	Endpoint	Description
GET	/	Informations sur l'API
POST	/generate/text	Génère du texte
POST	/generate/image	Génère une image
POST	/generate/video	Génère une vidéo
Exemples de requêtes
Générer du texte
Bash

curl -X POST http://localhost:8000/generate/text \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Bonjour, comment ça va ?"}'
Générer une image
Bash

curl -X POST http://localhost:8000/generate/image \
  -H "Content-Type: application/json" \
  -d '{"prompt": "A beautiful sunset", "style": "cinematic"}'
Documentation interactive
Accède à la documentation Swagger UI :

text

http://localhost:8000/docs
📁 Structure du projet
text

projet-ia-generative/
│
├── 📁 backend/
│   ├── 📄 main.py              # Point d'entrée FastAPI
│   ├── 📄 requirements.txt     # Dépendances Python
│   ├── 📄 Dockerfile           # Image Docker backend
│   ├── 📁 config/
│   │   └── settings.py         # Configuration
│   └── 📁 services/
│       ├── text_service.py     # Logique génération texte
│       ├── image_service.py    # Logique génération image
│       └── video_service.py    # Logique génération vidéo
│
├── 📁 frontend/
│   ├── 📄 Dockerfile           # Image Docker frontend
│   ├── 📄 nginx.conf           # Configuration Nginx
│   └── 📁 src/
│       └── 📁 app/
│           ├── app.component.ts
│           ├── app.component.html
│           └── app.component.scss
│
├── 📄 docker-compose.yml       # Orchestration Docker
└── 📄 README.md                # Ce fichier !
🗺 Roadmap
 Backend FastAPI
 Frontend Angular
 Génération de texte (Groq)
 Génération d'images (HuggingFace)
 Génération de vidéos (FFmpeg)
 Conteneurisation Docker
 Déploiement cloud
 CI/CD avec GitHub Actions
 Tests automatisés
 Authentification utilisateur
 Historique des générations
👨‍💻 Auteur
<div align="center">
Mohamed Dhia Khammar

GitHub
LinkedIn

</div>
📄 Licence
Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

<div align="center">
⭐ Si ce projet t'a plu, n'hésite pas à lui donner une étoile !

Made with ❤️ and ☕

</div>

