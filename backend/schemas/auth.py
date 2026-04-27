from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional

# ======================================================
# SCHEMAS D'INSCRIPTION
# ======================================================

class RegisterRequest(BaseModel):
    """
    Données reçues lors de l'inscription
    Pydantic valide automatiquement les types et contraintes
    """
    nom: str
    email: str
    password: str
    
    @field_validator('nom')
    def nom_must_not_be_empty(cls, v):
        if len(v.strip()) < 2:
            raise ValueError('Le nom doit avoir au moins 2 caractères')
        return v.strip()
    
    @field_validator('password')
    def password_must_be_strong(cls, v):
        if len(v) < 6:
            raise ValueError('Le mot de passe doit avoir au moins 6 caractères')
        return v
    
    @field_validator('email')
    def email_must_be_valid(cls, v):
        if '@' not in v:
            raise ValueError('Email invalide')
        return v.lower().strip()

# ======================================================
# SCHEMAS DE CONNEXION
# ======================================================

class LoginRequest(BaseModel):
    """
    Données reçues lors de la connexion
    """
    email: str
    password: str

# ======================================================
# SCHEMAS DE RÉPONSE
# ======================================================

class TokenResponse(BaseModel):
    """
    Réponse après inscription/connexion réussie
    On retourne le token et les infos de base
    """
    access_token: str
    token_type: str = "bearer"
    user_id: int
    nom: str
    email: str

class UserResponse(BaseModel):
    """
    Infos de l'utilisateur connecté
    On n'inclut JAMAIS le password_hash !
    """
    id: int
    nom: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True
        # Permet de convertir un objet SQLAlchemy en Pydantic