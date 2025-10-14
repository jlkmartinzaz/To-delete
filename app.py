from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config.settings import Config
from models import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Crear carpeta para la base de datos si no existe
    db_path = Config.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    db.init_app(app)
    JWTManager(app)

    # 🔹 Importa y registra los blueprints
    from controllers.auth_controller import auth_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")

    # Crear las tablas si no existen
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
