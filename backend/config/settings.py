import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings





# Charger les variables du fichier .env
load_dotenv()

class Settings(BaseSettings):
    GROQ_API_KEY: str = ""
    HF_API_KEY: str = ""
    UNSPLASH_ACCESS_KEY: str = ""
    OUTPUT_DIR: str = "output"
    
    # ✅ NOUVEAUX
    SECRET_KEY: str = "ma-cle-secrete-super-longue-2024-ia-generative"
    DATABASE_URL: str = "sqlite:///./app.db"
    
    class Config:
        env_file = ".env"

settings = Settings()