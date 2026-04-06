# ===== ÉTAPE 1 : Build Angular =====
FROM node:18-alpine AS build

WORKDIR /app

# Copier package.json d'abord (optimise le cache)
COPY package.json package-lock.json* ./

# Installer les dépendances
RUN npm install

# Copier le code source
COPY . .

# Build l'application Angular
RUN npm run build -- --configuration=production

# ===== ÉTAPE 2 : Servir avec Nginx =====
FROM nginx:alpine

# Copier la config Nginx personnalisée
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Copier les fichiers buildés depuis l'étape 1
COPY --from=build /app/dist/frontend/browser /usr/share/nginx/html

# Exposer le port
EXPOSE 80

# Lancer Nginx
CMD ["nginx", "-g", "daemon off;"]