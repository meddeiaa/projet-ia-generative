async def enhance_prompt(prompt: str, style: str = "general") -> str:
    """
    Améliore un prompt simple pour obtenir de meilleures images
    
    Args:
        prompt: Le prompt original de l'utilisateur
        style: Le style souhaité (general, photo, art, anime)
    
    Returns:
        Le prompt amélioré
    """
    
    # Mots-clés de qualité
    quality_keywords = "highly detailed, high quality, sharp focus, 8k"
    
    # Styles prédéfinis
    styles = {
        "general": f"{prompt}, {quality_keywords}, professional",
        
        "photo": f"{prompt}, professional photography, natural lighting, "
                 f"photorealistic, DSLR quality, {quality_keywords}",
        
        "art": f"{prompt}, digital art, illustration, vibrant colors, "
               f"artistic, trending on artstation, {quality_keywords}",
        
        "anime": f"{prompt}, anime style, studio ghibli, colorful, "
                 f"beautiful, detailed anime art, {quality_keywords}",
        
        "cinematic": f"{prompt}, cinematic lighting, dramatic atmosphere, "
                     f"movie scene, epic, {quality_keywords}",
        
        "fantasy": f"{prompt}, fantasy art, magical, ethereal, glowing, "
                   f"mystical atmosphere, {quality_keywords}",
        
        "realistic": f"{prompt}, photorealistic, hyperrealistic, "
                     f"ultra detailed, natural, {quality_keywords}"
    }
    
    # Retourner le prompt amélioré selon le style
    return styles.get(style, styles["general"])


def get_negative_prompt() -> str:
    """
    Retourne un negative prompt pour éviter les mauvais résultats
    """
    return (
        "blurry, low quality, distorted, deformed, ugly, bad anatomy, "
        "bad proportions, duplicate, error, jpeg artifacts, watermark, "
        "text, signature, username, low resolution"
    )