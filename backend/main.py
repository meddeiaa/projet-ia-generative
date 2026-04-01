from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

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

# Configurer CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "endpoints": {
            "texte": "/generate/text",
            "image": "/generate/image",
            "video": "/generate/video"
        },
        "styles_image": ["general", "photo", "art", "anime", "cinematic", "fantasy", "realistic"]
    }


@app.post("/generate/text", response_model=GenerateResponse)
async def api_generate_text(request: PromptRequest):
    """
    Génère du texte à partir d'un prompt
    
    - **prompt**: La question ou demande
    - **Retourne**: Le texte généré par LLaMA 3
    """
    try:
        result = await generate_text(request.prompt)
        return GenerateResponse(success=True, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/image", response_model=GenerateResponse)
async def api_generate_image(request: ImageRequest):
    """
    Génère une image avec l'IA
    
    - **prompt**: Description de l'image
    - **style**: Style artistique (general, photo, art, anime, cinematic, fantasy, realistic)
    - **Retourne**: Image en base64
    """
    try:
        result = await generate_image(request.prompt, request.style)
        return GenerateResponse(success=True, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/video")
async def api_generate_video(request: PromptRequest):
    """
    Génère une vidéo à partir d'un prompt
    
    - **prompt**: Thème de la vidéo
    - **Retourne**: Fichier vidéo MP4
    """
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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)