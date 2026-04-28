from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class User(Base):
    """
    Table 'users' dans la base de données
    
    Chaque ligne = un utilisateur inscrit
    """
    
    # Nom de la table dans la DB
    __tablename__ = "users"
    
    # ======================================================
    # COLONNES
    # ======================================================
    
    id = Column(
        Integer,
        primary_key=True,  # Identifiant unique
        index=True,        # Index pour chercher rapidement
        autoincrement=True # S'incrémente automatiquement
    )
    
    nom = Column(
        String(100),       # Max 100 caractères
        nullable=False     # Obligatoire
    )
    
    email = Column(
        String(255),
        unique=True,       # Un seul compte par email
        nullable=False,
        index=True         # Index car on cherche souvent par email
    )
    
    password_hash = Column(
        String(255),
        nullable=False
        # On stocke le HASH, jamais le mot de passe en clair !
    )
    
    is_active = Column(
        Boolean,
        default=True       # Compte actif par défaut
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow  # Date de création automatique
    )
    
    # ======================================================
    # RELATIONS
    # ======================================================
    # Un utilisateur peut avoir PLUSIEURS entrées d'historique
    # SQLAlchemy gère cette relation automatiquement
    
    history = relationship(
        "History",         # Nom du modèle lié
        back_populates="user",  # Référence inverse
        cascade="all, delete-orphan"
        # Si on supprime un user → son historique est supprimé aussi
    )
    
    def __repr__(self):
        return f"<User {self.email}>"