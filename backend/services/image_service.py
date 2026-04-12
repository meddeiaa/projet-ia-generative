import httpx
import base64
from config.settings import settings
from services.prompt_service import enhance_prompt, get_negative_prompt

async def generate_image(prompt: str, style: str = "general") -> str:
    """
    Génère une image avec l'IA (FLUX.1-schnell - Black Forest Labs)
    """
    try:
        # Améliorer le prompt
        enhanced_prompt = await enhance_prompt(prompt, style)
        
        print(f"🎨 Prompt original: {prompt}")
        print(f"🎨 Style: {style}")
        print(f"✨ Prompt amélioré: {enhanced_prompt}")
        
        # Vérifier la clé API
        if not settings.HF_API_KEY:
            raise Exception("HF_API_KEY non configurée dans .env")
        
        print(f"🔑 Clé API: {settings.HF_API_KEY[:10]}...")
        
        # ✅ NOUVEAU MODÈLE - FLUX.1-schnell (rapide, gratuit, haute qualité)
        API_URL = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-schnell"
        
        headers = {
            "Authorization": f"Bearer {settings.HF_API_KEY}"
        }
        
        print(f"📡 Appel API: {API_URL}")
        
        async with httpx.AsyncClient(timeout=120) as client:
            response = await client.post(
                API_URL,
                headers=headers,
                json={"inputs": enhanced_prompt}
            )
        
        print(f"📥 Status code: {response.status_code}")
        
        # Si FLUX.1-schnell ne marche pas, essayer FLUX.1-dev
        if response.status_code in [410, 503, 500]:
            print("⚠️ FLUX.1-schnell indisponible, essai avec FLUX.1-dev...")
            
            API_URL_FALLBACK = "https://router.huggingface.co/hf-inference/models/black-forest-labs/FLUX.1-dev"
            print(f"📡 Appel API fallback: {API_URL_FALLBACK}")
            
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    API_URL_FALLBACK,
                    headers=headers,
                    json={"inputs": enhanced_prompt}
                )
            
            print(f"📥 Status code fallback: {response.status_code}")
        
        # Si toujours en erreur, essayer stable-diffusion-3.5
        if response.status_code in [410, 503, 500]:
            print("⚠️ FLUX.1-dev indisponible, essai avec SD 3.5...")
            
            API_URL_FALLBACK2 = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-3.5-large"
            print(f"📡 Appel API fallback 2: {API_URL_FALLBACK2}")
            
            async with httpx.AsyncClient(timeout=120) as client:
                response = await client.post(
                    API_URL_FALLBACK2,
                    headers=headers,
                    json={"inputs": enhanced_prompt}
                )
            
            print(f"📥 Status code fallback 2: {response.status_code}")
        
        if response.status_code != 200:
            error_text = response.text
            print(f"❌ Erreur API: {error_text}")
            raise Exception(f"Erreur API ({response.status_code}): {error_text}")
        
        # Vérifier que c'est bien une image
        content_type = response.headers.get("content-type", "")
        print(f"📄 Content-Type: {content_type}")
        
        if "image" not in content_type and "application/json" in content_type:
            error_data = response.json()
            print(f"❌ Réponse JSON: {error_data}")
            raise Exception(f"API a retourné JSON au lieu d'une image: {error_data}")
        
        # Convertir en base64
        image_base64 = base64.b64encode(response.content).decode()
        
        print(f"✅ Image générée avec succès ({len(image_base64)} caractères)")
        
        return f"data:image/png;base64,{image_base64}"
    
    except httpx.TimeoutException:
        print("❌ Timeout: L'API a pris trop de temps")
        raise Exception("Timeout: La génération a pris trop de temps. Réessayez.")
    
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        raise Exception(f"Erreur génération image: {str(e)}")