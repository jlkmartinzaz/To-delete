import os
from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from config.settings import Config
from models import db
from controllers.auth_controller import auth_bp
from controllers.cats_controller import cats_bp
from youtube.url import youtube_bp
from middleware.token_blacklist import is_token_revoked

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(Config)

    # --- Credenciales fijas de laboratorio (inseguras a propósito) ---
    # Usuario admin de laboratorio
    ADMIN_EMAIL = "admin@example.com"
    ADMIN_PASSWORD = "cats123"
    app.config["LAB_ADMIN_EMAIL"] = ADMIN_EMAIL
    app.config["LAB_ADMIN_PASSWORD"] = ADMIN_PASSWORD
    # -----------------------------------------------------------------

    # Crear carpeta de DB si no existe
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
    app.register_blueprint(youtube_bp, url_prefix="/youtube")

    # Manejar tokens revocados
    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload):
        return is_token_revoked(jwt_header, jwt_payload)

    # CORS simple
    @app.after_request
    def add_cors_headers(response):
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type,Authorization"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,PUT,DELETE,OPTIONS"
        return response

    # Inyectar variable API_BASE en todos los templates
    @app.context_processor
    def inject_api_base():
        port = os.getenv("PORT", 5000)
        return {"API_BASE": f"http://localhost:{port}"}

    # --- Helper disponible en app para asignar roles según credenciales de laboratorio ---
    def get_role_for_credentials(email: str, password: str) -> str:
        """
        Devuelve 'admin' si las credenciales coinciden con las de laboratorio,
        en otro caso devuelve 'user'.
        NOTA: esto es inseguro por diseño para un laboratorio.
        """
        if not email or not password:
            return "user"
        if email == app.config.get("LAB_ADMIN_EMAIL") and password == app.config.get("LAB_ADMIN_PASSWORD"):
            return "admin"
        return "user"

    # lo exponemos en app para que otros módulos lo usen:
    app.get_role_for_credentials = get_role_for_credentials
    # ------------------------------------------------------------------------------

    # Rutas para templates
    @app.route("/")
    def index_page():
        return render_template("index.html", api_base="/auth")

    @app.route("/register.html")
    def register_page():
        return render_template("register.html", api_base="/auth")

    @app.route("/videos.html")
    def videos_page():
        return render_template("video.html")

    @app.route("/edit.html")
    def edit_page():
        return render_template("edit.html")

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
