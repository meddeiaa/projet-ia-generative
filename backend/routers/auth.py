from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database.database import get_db
from models.user import User
from schemas.auth import RegisterRequest, LoginRequest, TokenResponse, UserResponse
from auth.jwt import create_access_token
from auth.dependencies import get_current_user

# ======================================================
# CONFIGURATION
# ======================================================

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Contexte de hachage avec bcrypt
# bcrypt est l'algorithme recommandé pour les mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ======================================================
# FONCTIONS UTILITAIRES
# ======================================================

def hash_password(password: str) -> str:
    """
    Hache un mot de passe avec bcrypt
    
    "monMotDePasse" → "$2b$12$KIX9..."
    
    Le hash est IRRÉVERSIBLE :
    On ne peut pas retrouver le mot de passe depuis le hash
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie si un mot de passe correspond à son hash
    
    bcrypt.verify("monMotDePasse", "$2b$12$KIX9...") → True
    bcrypt.verify("mauvaisMotDePasse", "$2b$12$KIX9...") → False
    """
    return pwd_context.verify(plain_password, hashed_password)

# ======================================================
# ROUTES
# ======================================================

@router.post("/register", response_model=TokenResponse, status_code=201)
async def register(request: RegisterRequest, db: Session = Depends(get_db)):
    """
    Inscription d'un nouvel utilisateur
    
    ÉTAPES :
    1. Vérifier si l'email est déjà utilisé
    2. Hacher le mot de passe
    3. Créer l'utilisateur dans la DB
    4. Créer et retourner un JWT token
    """
    
    # Étape 1 : Vérifier si l'email existe déjà
    existing_user = db.query(User).filter(
        User.email == request.email.lower()
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Un compte avec cet email existe déjà"
        )
    
    # Étape 2 : Hacher le mot de passe
    hashed_pwd = hash_password(request.password)
    
    # Étape 3 : Créer l'utilisateur
    new_user = User(
        nom=request.nom,
        email=request.email.lower(),
        password_hash=hashed_pwd
    )
    
    db.add(new_user)      # Ajoute à la session
    db.commit()           # Sauvegarde dans la DB
    db.refresh(new_user)  # Récupère l'ID auto-généré
    
    # Étape 4 : Créer le token JWT
    token = create_access_token({
        "user_id": new_user.id,
        "email": new_user.email
    })
    
    return TokenResponse(
        access_token=token,
        user_id=new_user.id,
        nom=new_user.nom,
        email=new_user.email
    )


@router.post("/login", response_model=TokenResponse)
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    """
    Connexion d'un utilisateur existant
    
    ÉTAPES :
    1. Chercher l'utilisateur par email
    2. Vérifier le mot de passe
    3. Créer et retourner un JWT token
    """
    
    # Étape 1 : Chercher l'utilisateur
    user = db.query(User).filter(
        User.email == request.email.lower()
    ).first()
    
    # Étape 2 : Vérifier le mot de passe
    # On retourne TOUJOURS la même erreur
    # Pour ne pas révéler si l'email existe ou non
    if not user or not verify_password(request.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Compte désactivé"
        )
    
    # Étape 3 : Créer le token
    token = create_access_token({
        "user_id": user.id,
        "email": user.email
    })
    
    return TokenResponse(
        access_token=token,
        user_id=user.id,
        nom=user.nom,
        email=user.email
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Retourne les infos de l'utilisateur connecté
    
    Cette route est PROTÉGÉE :
    └── Nécessite un token valide dans le Header
        Authorization: Bearer eyJhbG...
    """
    return current_user