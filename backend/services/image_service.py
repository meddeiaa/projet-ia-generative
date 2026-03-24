import httpx
import base64
from config.settings import settings

async def generate_image(prompt: str) -> str:
    """
    Génère une image avec Hugging Face (SDXL)
    """
    try:
        # NOUVELLE URL
        API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
        
        headers = {
            "Authorization": f"Bearer {settings.HF_API_KEY}"
        }
        
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                API_URL,
                headers=headers,
                json={"inputs": prompt}
            )
        
        if response.status_code != 200:
            raise Exception(f"Erreur API: {response.text}")
        
        image_base64 = base64.b64encode(response.content).decode()
        
        return f"data:image/png;base64,{image_base64}"
    
    except Exception as e:
        raise Exception(f"Erreur génération image: {str(e)}")


async def generate_image_free(prompt: str) -> str:
    """
    Génère une image avec Pollinations (gratuit)
    """
    prompt_encoded = prompt.replace(" ", "%20")
    return f"https://image.pollinations.ai/prompt/{prompt_encoded}"