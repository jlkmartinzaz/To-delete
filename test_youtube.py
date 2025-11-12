# test_youtube_input.py
import os
import requests
import re
from config.config import Config

def extract_video_id(url: str):
    """Extrae el ID del video de la URL de YouTube"""
    pattern = r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})"
    m = re.search(pattern, url)
    return m.group(1) if m else None

def main():
    api_key = Config.YOUTUBE_API_KEY
    if not api_key:
        print("❌ YOUTUBE_API_KEY no está definida")
        return

    url = input("Ingresa la URL de YouTube: ").strip()
    vid_id = extract_video_id(url)
    if not vid_id:
        print("❌ URL inválida")
        return

    api_url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&id={vid_id}&key={api_key}"

    try:
        res = requests.get(api_url)
        res.raise_for_status()
        data = res.json()
        if "items" in data and data["items"]:
            item = data["items"][0]
            print("✅ Video encontrado")
            print("Título:", item["snippet"]["title"])
            print("Descripción:", item["snippet"]["description"])
            print("Likes:", item["statistics"].get("likeCount", 0))
        else:
            print("❌ Video no encontrado")
    except requests.exceptions.HTTPError as e:
        print("❌ Error HTTP:", e)
        print(res.json())
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
