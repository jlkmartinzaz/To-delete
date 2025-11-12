import os
from flask import Flask, jsonify, render_template
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

    # Crear carpeta para la base de datos (seguro y anticipado)
    db_path = app.config["SQLALCHEMY_DATABASE_URI"].replace("sqlite:///", "")
    db_dir = os.path.dirname(db_path)
    os.makedirs(db_dir, exist_ok=True)
    os.chmod(db_dir, 0o777)

    # Inicializar extensiones
    db.init_app(app)
    jwt = JWTManager(app)

    # Registrar blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(cats_bp, url_prefix="/cats")

    # Manejar tokens revocados
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_header, jwt_payload)

    @app.route("/")
    def index():
        return render_template("index.html")

    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
