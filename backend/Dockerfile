# ===== BACKEND DOCKERFILE =====
# Image Python légère
FROM python:3.11-slim

# Installer FFmpeg (pour la génération vidéo)
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir le dossier de travail
WORKDIR /app

# Copier les dépendances d'abord (optimise le cache Docker)
COPY requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier tout le code
COPY . .

# Créer le dossier output
RUN mkdir -p output

# Exposer le port
EXPOSE 8000

# Lancer le serveur
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]