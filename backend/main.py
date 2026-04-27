from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from sqlalchemy.orm import Session
import os

# Importer les services
from services.text_service import generate_text
from services.image_service import generate_image
from services.video_service import generate_video

# Importer la DB
from database.database import engine, get_db
from models.user import User
from models.history import History
import models.user
import models.history

# Importer les routers
from routers.auth import router as auth_router
from routers.history import router as history_router

# Importer l'auth
from auth.dependencies import get_current_user

# ======================================================
# CRÉER LES TABLES
# ======================================================
# Crée automatiquement les tables si elles n'existent pas
# En production avec Alembic, on ferait des migrations
models.user.Base.metadata.create_all(bind=engine)
models.history.Base.metadata.create_all(bind=engine)

# ======================================================
# APPLICATION
# ======================================================

app = FastAPI(
    title="API IA Générative",
    description="API pour générer du texte, des images et des vidéos avec l'IA",
    version="2.0.0"
)

# ======================================================
# CORS
# ======================================================

FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if FRONTEND_URL != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ======================================================
# ROUTERS
# ======================================================

# Inclure les routes d'authentification
app.include_router(auth_router)

# Inclure les routes d'historique
app.include_router(history_router)

# ======================================================
# MODÈLES DE DONNÉES
# ======================================================

class PromptRequest(BaseModel):
    prompt: str

class ImageRequest(BaseModel):
    prompt: str
    style: Optional[str] = "general"

class GenerateResponse(BaseModel):
    success: bool
    result: str

# ======================================================
# ENDPOINTS PUBLICS
# ======================================================

@app.get("/")
async def root():
    return {
        "message": "Bienvenue sur l'API IA Générative !",
        "version": "2.0.0",
        "status": "online",
        "features": ["text", "image", "video", "auth", "history"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy"}

# ======================================================
# ENDPOINTS PROTÉGÉS (nécessitent un token JWT)
# ======================================================

@app.post("/generate/text", response_model=GenerateResponse)
async def api_generate_text(
    request: PromptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Génère du texte - PROTÉGÉ
    Nécessite : Authorization: Bearer TOKEN
    """
    try:
        result = await generate_text(request.prompt)
        
        # Sauvegarder dans l'historique
        history_item = History(
            user_id=current_user.id,
            generation_type="text",
            prompt=request.prompt,
            result=result
        )
        db.add(history_item)
        db.commit()
        
        return GenerateResponse(success=True, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/image", response_model=GenerateResponse)
async def api_generate_image(
    request: ImageRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Génère une image - PROTÉGÉ
    """
    try:
        result = await generate_image(request.prompt, request.style)
        
        # Sauvegarder dans l'historique
        history_item = History(
            user_id=current_user.id,
            generation_type="image",
            prompt=request.prompt,
            style=request.style,
            result=result  # Image en base64
        )
        db.add(history_item)
        db.commit()
        
        return GenerateResponse(success=True, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/video")
async def api_generate_video(
    request: PromptRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Génère une vidéo - PROTÉGÉ
    """
    try:
        video_path = await generate_video(request.prompt)
        
        # Sauvegarder dans l'historique
        history_item = History(
            user_id=current_user.id,
            generation_type="video",
            prompt=request.prompt,
            result=video_path
        )
        db.add(history_item)
        db.commit()
        
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename="generated_video.mp4"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)