from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database.database import Base

class History(Base):
    """
    Table 'history' dans la base de données
    
    Chaque ligne = une génération (texte, image, ou vidéo)
    """
    
    __tablename__ = "history"
    
    # ======================================================
    # COLONNES
    # ======================================================
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    user_id = Column(
        Integer,
        ForeignKey("users.id"),  # Clé étrangère → table users
        nullable=False
        # Chaque entrée appartient à UN utilisateur
    )
    
    generation_type = Column(
        String(20),
        nullable=False
        # "text", "image", ou "video"
    )
    
    prompt = Column(
        Text,              # Text = string illimitée
        nullable=False
    )
    
    style = Column(
        String(50),
        nullable=True      # Seulement pour les images
        # "cinematic", "anime", etc.
    )
    
    result = Column(
        Text,
        nullable=True
        # Pour texte : le texte généré
        # Pour image : l'image en base64
        # Pour vidéo : le chemin du fichier
    )
    
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
    
    # ======================================================
    # RELATIONS
    # ======================================================
    # Chaque historique appartient à UN utilisateur
    
    user = relationship(
        "User",
        back_populates="history"
    )
    
    def __repr__(self):
        return f"<History {self.generation_type} by user {self.user_id}>"