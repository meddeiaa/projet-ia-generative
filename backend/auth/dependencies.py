from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database.database import get_db
from models.user import User
from auth.jwt import verify_token

# ======================================================
# SCHÉMA DE SÉCURITÉ
# ======================================================

# HTTPBearer = lit le token depuis le Header Authorization
# Le client doit envoyer : Authorization: Bearer eyJhbG...
security = HTTPBearer()

# ======================================================
# DÉPENDANCE : UTILISATEUR CONNECTÉ
# ======================================================

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """
    Dépendance FastAPI pour obtenir l'utilisateur connecté
    
    COMMENT ÇA MARCHE :
    1. FastAPI lit le Header "Authorization: Bearer TOKEN"
    2. On extrait le TOKEN
    3. On vérifie le TOKEN avec notre clé secrète
    4. On récupère l'utilisateur depuis la DB
    5. On le retourne à la route
    
    USAGE DANS UNE ROUTE :
    @app.get("/protected")
    def protected_route(user = Depends(get_current_user)):
        return {"message": f"Bonjour {user.nom}"}
    
    Si le token est invalide → 401 Unauthorized automatiquement
    """
    
    # Définit l'erreur à retourner si non authentifié
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token invalide ou expiré",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Extrait le token du header
    token = credentials.credentials
    
    
    # Vérifie et décode le token
    payload = verify_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extrait l'user_id du token
    user_id = payload.get("user_id")
    if user_id is None:
        raise credentials_exception
    
    # Récupère l'utilisateur depuis la DB
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception
    
    # Vérifie que le compte est actif
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compte désactivé"
        )
    
    return user