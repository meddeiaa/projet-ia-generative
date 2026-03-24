import os

from dotenv import load_dotenv




# Charger les variables du fichier .env
load_dotenv()

class Settings:
    """Configuration de l'application"""
    
    # Clés API
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    HF_API_KEY: str = os.getenv("HF_API_KEY", "")
    
    # Dossier pour les fichiers générés
    OUTPUT_DIR: str = "output"

# Instance unique de la configuration
settings = Settings()