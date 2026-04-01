import subprocess
import os
import httpx
import random
from config.settings import settings

async def generate_video(prompt: str, num_images: int = 5) -> str:
    """
    Génère une vidéo cinématique avec effets professionnels
    """
    try:
        output_dir = settings.OUTPUT_DIR
        os.makedirs(output_dir, exist_ok=True)
        
        images = []
        
        base_style = "cinematic, highly detailed, professional photography, 8k quality"
        
        variations = [
            f"{prompt}, wide establishing shot, {base_style}",
            f"{prompt}, medium shot, slightly different angle, {base_style}",
            f"{prompt}, close-up detail, {base_style}",
            f"{prompt}, dramatic side lighting, {base_style}",
            f"{prompt}, golden hour lighting, epic finale, {base_style}"
        ]
        
        print("🎬 Génération des images cinématiques...")
        print(f"   Thème: {prompt}")
        
        # ✅ URL CORRIGÉE - API gratuite
        API_URL = "https://router.huggingface.co/hf-inference/models/stabilityai/stable-diffusion-xl-base-1.0"
        headers = {"Authorization": f"Bearer {settings.HF_API_KEY}"}
        
        for i in range(min(num_images, len(variations))):
            try:
                print(f"  📸 Image {i+1}/{num_images}...")
                
                async with httpx.AsyncClient(timeout=120) as client:
                    response = await client.post(
                        API_URL,
                        headers=headers,
                        json={"inputs": variations[i]}
                    )
                
                if response.status_code == 200:
                    image_path = os.path.join(output_dir, f"frame_{i}.png")
                    with open(image_path, "wb") as f:
                        f.write(response.content)
                    images.append(image_path)
                    print(f"  ✅ Image {i+1}/{num_images} générée")
                else:
                    print(f"  ⚠️ Erreur image {i+1}: {response.status_code}")
                    
            except Exception as e:
                print(f"  ⚠️ Erreur: {str(e)}")
                continue
        
        if len(images) < 2:
            raise Exception(f"Seulement {len(images)} image(s). Réessayez.")
        
        # ===== Le reste du code reste IDENTIQUE =====
        print(f"🎬 Création de {len(images)} clips avec effets Ken Burns...")
        
        ken_burns_effects = [
            "zoompan=z='min(zoom+0.0015,1.5)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=90:s=1280x720:fps=30",
            "zoompan=z='if(lte(zoom,1.0),1.5,max(1.001,zoom-0.0015))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=90:s=1280x720:fps=30",
            "zoompan=z='1.3':x='if(lte(on,1),0,x+1)':y='ih/2-(ih/zoom/2)':d=90:s=1280x720:fps=30",
            "zoompan=z='1.3':x='if(lte(on,1),iw,x-1)':y='ih/2-(ih/zoom/2)':d=90:s=1280x720:fps=30",
            "zoompan=z='min(zoom+0.0015,1.5)':x='iw/4-(iw/zoom/4)':y='ih/4-(ih/zoom/4)':d=90:s=1280x720:fps=30"
        ]
        
        temp_clips = []
        
        for i, img in enumerate(images):
            clip_path = os.path.join(output_dir, f"clip_{i}.mp4")
            effect = ken_burns_effects[i % len(ken_burns_effects)]
            
            cmd = [
                "ffmpeg", "-y",
                "-loop", "1",
                "-i", img,
                "-vf", f"scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,{effect},format=yuv420p",
                "-t", "3",
                "-c:v", "libx264",
                "-preset", "medium",
                "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-r", "30",
                clip_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0 and os.path.exists(clip_path):
                temp_clips.append(clip_path)
                print(f"  ✅ Clip {i+1}/{len(images)} créé avec effet Ken Burns")
            else:
                print(f"  ⚠️ Erreur clip {i+1}: {result.stderr[:100] if result.stderr else 'unknown'}")
        
        if len(temp_clips) < 2:
            raise Exception("Impossible de créer assez de clips")
        
        print("🎬 Assemblage avec transitions en fondu...")
        
        video_path = os.path.join(output_dir, "output.mp4")
        
        if len(temp_clips) == 2:
            cmd = [
                "ffmpeg", "-y",
                "-i", temp_clips[0],
                "-i", temp_clips[1],
                "-filter_complex", "[0:v][1:v]xfade=transition=fade:duration=0.5:offset=2.5[v]",
                "-map", "[v]",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
        else:
            filter_parts = []
            filter_parts.append(f"[0:v][1:v]xfade=transition=fade:duration=0.5:offset=2.5[v1]")
            
            for i in range(2, len(temp_clips)):
                prev_label = f"v{i-1}"
                next_label = f"v{i}" if i < len(temp_clips) - 1 else "v"
                offset = 2.5 + (i - 1) * 2.5
                filter_parts.append(f"[{prev_label}][{i}:v]xfade=transition=fade:duration=0.5:offset={offset}[{next_label}]")
            
            filter_complex = ";".join(filter_parts)
            
            cmd = ["ffmpeg", "-y"]
            for clip in temp_clips:
                cmd.extend(["-i", clip])
            cmd.extend([
                "-filter_complex", filter_complex,
                "-map", "[v]",
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                video_path
            ])
            
            result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode != 0 or not os.path.exists(video_path):
            print("  ⚠️ Crossfade échoué, utilisation concat simple...")
            
            list_file = os.path.join(output_dir, "clips.txt")
            with open(list_file, "w", encoding="utf-8") as f:
                for clip in temp_clips:
                    abs_path = os.path.abspath(clip).replace("\\", "/")
                    f.write(f"file '{abs_path}'\n")
            
            cmd = [
                "ffmpeg", "-y",
                "-f", "concat",
                "-safe", "0",
                "-i", list_file,
                "-c:v", "libx264",
                "-pix_fmt", "yuv420p",
                video_path
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            try: os.remove(list_file)
            except: pass
        
        if not os.path.exists(video_path):
            raise Exception("Impossible de créer la vidéo finale")
        
        print("🎨 Application du color grading cinématique...")
        
        final_video = os.path.join(output_dir, "final_output.mp4")
        
        color_cmd = [
            "ffmpeg", "-y",
            "-i", video_path,
            "-vf", "eq=contrast=1.1:brightness=0.02:saturation=1.2,colorbalance=rs=0.1:gs=0.05:bs=-0.1",
            "-c:v", "libx264",
            "-preset", "medium",
            "-crf", "20",
            "-pix_fmt", "yuv420p",
            final_video
        ]
        
        result = subprocess.run(color_cmd, capture_output=True, text=True)
        
        if result.returncode == 0 and os.path.exists(final_video):
            os.remove(video_path)
            os.rename(final_video, video_path)
            print("  ✅ Color grading appliqué!")
        else:
            print("  ⚠️ Color grading échoué, vidéo sans effet")
        
        print(f"🎉 Vidéo finale créée: {video_path}")
        
        for img in images:
            try: os.remove(img)
            except: pass
        for clip in temp_clips:
            try: os.remove(clip)
            except: pass
        
        size = os.path.getsize(video_path) / (1024 * 1024)
        print(f"  📊 Taille: {size:.2f} MB")
        
        return video_path
        
    except Exception as e:
        error_msg = str(e) if str(e) else "Erreur inconnue"
        print(f"❌ Erreur: {error_msg}")
        raise Exception(error_msg)


async def generate_video_simple(prompt: str) -> str:
    """
    Version simplifiée pour tester rapidement (2 images seulement)
    """
    return await generate_video(prompt, num_images=2)