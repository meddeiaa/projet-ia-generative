from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import os

# Importer les services
from services.text_service import generate_text
from services.image_service import generate_image
from services.video_service import generate_video

# Créer l'application
app = FastAPI(
    title="API IA Générative",
    description="API pour générer du texte, des images et des vidéos avec l'IA",
    version="1.0.0"
)

# ✅ CORS adapté pour le déploiement
# En local → accepte tout
# En production → accepte seulement l'URL du frontend
FRONTEND_URL = os.getenv("FRONTEND_URL", "*")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL] if FRONTEND_URL != "*" else ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ===== MODÈLES DE DONNÉES =====

class PromptRequest(BaseModel):
    prompt: str

class ImageRequest(BaseModel):
    prompt: str
    style: Optional[str] = "general"

class GenerateResponse(BaseModel):
    success: bool
    result: str

# ===== ENDPOINTS =====

@app.get("/")
async def root():
    """Page d'accueil de l'API"""
    return {
        "message": "Bienvenue sur l'API IA Générative !",
        "status": "online",
        "endpoints": {
            "texte": "/generate/text",
            "image": "/generate/image",
            "video": "/generate/video"
        },
        "styles_image": ["general", "photo", "art", "anime", "cinematic", "fantasy", "realistic"]
    }


# ✅ NOUVEAU : Health check pour Render
@app.get("/health")
async def health():
    """
    Render envoie une requête ici pour vérifier que l'app est vivante
    Si on répond 200 OK → app est saine
    Si on répond pas → Render redémarre l'app
    """
    return {"status": "healthy"}


@app.post("/generate/text", response_model=GenerateResponse)
async def api_generate_text(request: PromptRequest):
    """Génère du texte à partir d'un prompt"""
    try:
        result = await generate_text(request.prompt)
        return GenerateResponse(success=True, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/image", response_model=GenerateResponse)
async def api_generate_image(request: ImageRequest):
    """Génère une image avec l'IA"""
    try:
        result = await generate_image(request.prompt, request.style)
        return GenerateResponse(success=True, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/video")
async def api_generate_video(request: PromptRequest):
    """Génère une vidéo à partir d'un prompt"""
    try:
        video_path = await generate_video(request.prompt)
        return FileResponse(
            video_path,
            media_type="video/mp4",
            filename="generated_video.mp4"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ===== LANCER LE SERVEUR =====

if __name__ == "__main__":
    import uvicorn
    # ✅ Render injecte la variable PORT automatiquement
    # En local → 8000 (valeur par défaut)
    # Sur Render → le port qu'ils choisissent
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)