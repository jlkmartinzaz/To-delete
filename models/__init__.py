from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user_model import User  # ✅ nombre correcto del archivo
