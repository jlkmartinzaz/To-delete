# app.py
import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config.settings import Config
from models import db
from controllers.auth_controller import auth_bp
from controllers.cats_controller import cats_bp
from middleware.token_blacklist import is_token_revoked

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Crear carpeta para la DB si no existe
    db_path = Config.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    os.chmod(os.path.dirname(db_path), 0o755)

    # Inicializar extensiones
    db.init_app(app)
    jwt = JWTManager(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cats_bp, url_prefix="/cats")

    # Configurar token revocado (logout)
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_header, jwt_payload)

    # Manejo global de errores
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Ruta no encontrada"}), 404

    # Crear tablas
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
