from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

# Importer les services
from services.text_service import generate_text
from services.image_service import generate_image, generate_image_free
from services.video_service import generate_video

# Créer l'application FastAPI
app = FastAPI(
    title="API IA Générative",
    description="API pour générer du texte, des images et des vidéos avec l'IA",
    version="1.0.0"
)

# Configurer CORS (permet au frontend d'appeler le backend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # Autoriser tous les domaines
    allow_credentials=True,
    allow_methods=["*"],        # Autoriser toutes les méthodes
    allow_headers=["*"],        # Autoriser tous les headers
)

# ===== MODÈLES DE DONNÉES =====

class PromptRequest(BaseModel):
    """Requête avec un prompt"""
    prompt: str

class GenerateResponse(BaseModel):
    """Réponse avec le résultat"""
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
            "image_gratuite": "/generate/image-free",
            "video": "/generate/video"
        }
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
async def api_generate_image(request: PromptRequest):
    """
    Génère une image à partir d'un prompt (Hugging Face)
    
    - **prompt**: Description de l'image
    - **Retourne**: Image en base64
    """
    try:
        result = await generate_image(request.prompt)
        return GenerateResponse(success=True, result=result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/generate/image-free", response_model=GenerateResponse)
async def api_generate_image_free(request: PromptRequest):
    """
    Génère une image à partir d'un prompt (Pollinations - gratuit)
    
    - **prompt**: Description de l'image
    - **Retourne**: URL de l'image
    """
    try:
        result = await generate_image_free(request.prompt)
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
    
@app.post("/generate/video-quick")
async def api_generate_video_quick(request: PromptRequest):
    """
    Génère une vidéo rapide (2 images seulement)
    Plus rapide mais moins de contenu
    """
    try:
        from services.video_service import generate_video_simple
        video_path = await generate_video_simple(request.prompt)
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