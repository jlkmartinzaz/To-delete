# config/settings.py
import os
import datetime
from dotenv import load_dotenv

load_dotenv()

# ==============================
# Directorios dinámicos
# ==============================
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.getenv("DATA_DIR", os.path.join(BASE_DIR, "data"))
os.makedirs(DATA_DIR, exist_ok=True)

# ==============================
# Base de datos
# ==============================
# La URI se toma primero de variables de entorno
DATABASE_URL = os.getenv("DATABASE_URL")  # para local
SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")  # para Docker

# Si no hay variables de entorno, se usan rutas dinámicas
if not DATABASE_URL and not SQLALCHEMY_DATABASE_URI:
    default_db_path = os.path.join(DATA_DIR, "database.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{default_db_path}"

USE_DOCKER = os.getenv("USE_DOCKER", "false").lower() == "true"
SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI if USE_DOCKER else DATABASE_URL or SQLALCHEMY_DATABASE_URI

# ==============================
# Configuración de la app
# ==============================
class Config:
    # Seguridad
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    if not SECRET_KEY or not JWT_SECRET_KEY:
        raise ValueError("Debes definir SECRET_KEY y JWT_SECRET_KEY en las variables de entorno")

    # Base de datos
    SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Expiración de tokens
    JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(minutes=int(os.getenv("JWT_ACCESS_MINUTES", 2)))
    JWT_REFRESH_TOKEN_EXPIRES = datetime.timedelta(minutes=int(os.getenv("JWT_REFRESH_MINUTES", 5)))

    PROPAGATE_EXCEPTIONS = True

    @staticmethod
    def init_app(app):
        app.logger.info(f"Base de datos en uso: {Config.SQLALCHEMY_DATABASE_URI}")
        app.logger.info(f"Carpeta de datos: {DATA_DIR}")
