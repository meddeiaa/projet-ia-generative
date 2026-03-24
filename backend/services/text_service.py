from groq import Groq
from config.settings import settings

# Créer le client Groq
client = Groq(api_key=settings.GROQ_API_KEY)

async def generate_text(prompt: str) -> str:
    """
    Génère du texte avec Groq (LLaMA 3.3)
    
    Args:
        prompt: La question ou demande de l'utilisateur
    
    Returns:
        Le texte généré par l'IA
    """
    try:
        # Appeler l'API Groq
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",  # ✅ Nouveau modèle
            messages=[
                {
                    "role": "system",
                    "content": "Tu es un assistant utile. Réponds en français de manière claire et concise."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        # Extraire et retourner la réponse
        return response.choices[0].message.content
    
    except Exception as e:
        raise Exception(f"Erreur génération texte: {str(e)}")