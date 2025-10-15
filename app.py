from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from config.settings import Config
from models import db
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db_path = Config.SQLALCHEMY_DATABASE_URI.replace("sqlite:///", "")
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    os.chmod(os.path.dirname(db_path), 0o755)  # permisos seguros

    db.init_app(app)
    JWTManager(app)

    # Blueprints
    from controllers.auth_controller import auth_bp
    from controllers.cats_controller import cats_bp
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cats_bp, url_prefix="/cats")

    # Crear tablas
    with app.app_context():
        db.create_all()

    # Manejo global de errores
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Ruta no encontrada"}), 404

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
