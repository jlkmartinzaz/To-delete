import os
from dotenv import load_dotenv
import datetime
load_dotenv()

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DB_DIR, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default_jwt_secret")
    BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")
    DB_DIR = os.path.join(BASE_DIR, "data")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "SQLALCHEMY_DATABASE_URI",
        f"sqlite:///{os.path.join(DB_DIR, 'database.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Expiraciones en segundos
    JWT_ACCESS_TOKEN_EXPIRES = 120        # 2 minutos
    JWT_REFRESH_TOKEN_EXPIRES = 300       # 5 minutos