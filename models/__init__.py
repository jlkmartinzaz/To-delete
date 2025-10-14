from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# importa los modelos solo si es necesario al final
from .auth_model import User
from .cats_model import Cat
