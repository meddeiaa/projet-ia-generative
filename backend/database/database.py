from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# ======================================================
# CONFIGURATION DE LA BASE DE DONNÉES
# ======================================================

# En local    → SQLite (fichier simple, pas besoin d'installation)
# En prod     → PostgreSQL (Render offre ça gratuitement)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./app.db"  # Fichier app.db créé automatiquement
)

# ======================================================
# POURQUOI DEUX CONFIGS ?
# ======================================================
# SQLite et PostgreSQL ont des comportements légèrement
# différents. Pour SQLite, on doit activer check_same_thread=False
# Pour PostgreSQL, pas besoin de cette option

if DATABASE_URL.startswith("sqlite"):
    # Configuration SQLite (développement local)
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
        # check_same_thread=False permet d'utiliser
        # la même connexion depuis plusieurs threads
        # FastAPI est asynchrone donc nécessaire
    )
else:
    # Configuration PostgreSQL (production)
    # Render donne une URL qui commence par "postgres://"
    # mais SQLAlchemy veut "postgresql://"
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://", "postgresql://", 1
        )
    engine = create_engine(DATABASE_URL)

# ======================================================
# SESSION
# ======================================================
# SessionLocal = usine à sessions
# Chaque requête HTTP obtient sa propre session DB
# La session se ferme quand la requête se termine

SessionLocal = sessionmaker(
    autocommit=False,  # On valide manuellement les transactions
    autoflush=False,   # Pas de flush automatique
    bind=engine
)

# ======================================================
# BASE
# ======================================================
# Tous nos modèles (User, History) héritent de Base
# SQLAlchemy utilise Base pour créer les tables

Base = declarative_base()

# ======================================================
# DEPENDENCY INJECTION
# ======================================================
# FastAPI utilise ce pattern pour gérer les sessions
# Chaque route qui a besoin de la DB reçoit une session

def get_db():
    """
    Générateur de session DB
    
    Utilisé comme dépendance dans les routes FastAPI :
    def ma_route(db: Session = Depends(get_db)):
    
    La session est automatiquement fermée après la requête
    même si une erreur se produit (grâce au try/finally)
    """
    db = SessionLocal()
    try:
        yield db        # Donne la session à la route
    finally:
        db.close()      # Ferme toujours la session après