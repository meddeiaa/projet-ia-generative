# ===== BACKEND DOCKERFILE =====

# On part d'une image Python légère
# "slim" = version minimale, moins lourde
FROM python:3.11-slim

# Installer FFmpeg pour la génération vidéo
# apt-get = gestionnaire de paquets Linux (comme npm mais pour Linux)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir le dossier de travail dans le conteneur
WORKDIR /app

# Copier requirements.txt EN PREMIER
# Pourquoi ? Optimisation du cache Docker :
# Si le code change mais pas requirements.txt
# → Docker réutilise le cache pip (plus rapide !)
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le reste du code
COPY . .

# Créer le dossier output pour les vidéos générées
RUN mkdir -p output

# Documenter le port (informatif, pas obligatoire)
EXPOSE 8000

# ✅ MODIFIÉ : Utilise ${PORT} de Render
# En local  → PORT n'existe pas → utilise 8000
# Sur Render → PORT = leur port → utilise leur port
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}