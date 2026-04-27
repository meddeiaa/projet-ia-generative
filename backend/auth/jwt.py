from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
import os

# ======================================================
# CONFIGURATION JWT
# ======================================================

# Clé secrète pour signer les tokens
# En production → utilise une vraie clé secrète longue et aléatoire
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "ma-cle-secrete-super-longue-2024-ia-generative"
)

# Algorithme de signature
ALGORITHM = "HS256"
# HS256 = HMAC avec SHA-256
# Un des algorithmes les plus utilisés pour JWT

# Durée de validité du token : 24 heures
ACCESS_TOKEN_EXPIRE_HOURS = 24

# ======================================================
# CRÉER UN TOKEN
# ======================================================

def create_access_token(data: dict) -> str:
    """
    Crée un JWT token
    
    EXEMPLE :
    data = {"user_id": 1, "email": "a@gmail.com"}
    token = create_access_token(data)
    → "eyJhbGciOiJIUzI1NiJ9.eyJ1c2VySWQiOjF9.abc123"
    
    Le token contient :
    ├── Les données (user_id, email)
    ├── La date d'expiration
    └── Une signature cryptographique
    """
    
    # Copie les données pour ne pas modifier l'original
    to_encode = data.copy()
    
    # Calcule la date d'expiration
    expire = datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
    
    # Ajoute l'expiration aux données
    to_encode.update({"exp": expire})
    
    # Crée et retourne le token signé
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

# ======================================================
# VÉRIFIER UN TOKEN
# ======================================================

def verify_token(token: str) -> Optional[dict]:
    """
    Vérifie et décode un JWT token
    
    Retourne les données si le token est valide
    Retourne None si le token est invalide ou expiré
    
    VÉRIFICATIONS AUTOMATIQUES :
    ├── La signature est-elle correcte ?
    ├── Le token est-il expiré ?
    └── Le format est-il correct ?
    """
    try:
        # Décode et vérifie le token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        # Token invalide ou expiré
        return None