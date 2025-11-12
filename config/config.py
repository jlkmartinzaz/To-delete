# config/config.py
import os
from dotenv import load_dotenv
from config.settings import Config as SettingsConfig

load_dotenv()

class Config(SettingsConfig):
    # Solo agregamos variables específicas de YouTube y proxy
    YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
    YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

    USE_REVERSE_PROXY = os.getenv("USE_REVERSE_PROXY", "false").lower() == "true"

    @staticmethod
    def init_app(app):
        SettingsConfig.init_app(app)
        print(f"🔹 YouTube API Key: {Config.YOUTUBE_API_KEY}")
        print(f"🔹 Uso de Reverse Proxy: {Config.USE_REVERSE_PROXY}")
