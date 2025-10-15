# controllers/auth_controller.py
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from models.user_model import User
from models import db
import datetime

# Lista negra de tokens
BLACKLIST = set()

auth_bp = Blueprint("auth_bp", __name__)

# -------------------------------
# Registro de usuario
# -------------------------------
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "El usuario ya existe"}), 400

    user = User(email=email)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "Usuario creado correctamente"}), 201

# -------------------------------
# Login
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email y contraseña son obligatorios"}), 400

    # Buscar usuario en la base de datos
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Crear access token (corto) y refresh token (largo)
    access_token = create_access_token(
        identity=str(user.id),          # siempre como string
        additional_claims={"role": user.role},  
        expires_delta=datetime.timedelta(seconds=120)  # 2 minutos
    )
    refresh_token = create_refresh_token(
        identity=str(user.id),
        expires_delta=datetime.timedelta(seconds=300)  # 5 minutos
    )

    # Devolver tokens y datos públicos del usuario
    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_safe_dict()
    }), 200

# -------------------------------
# Logout
# -------------------------------
@auth_bp.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    """
    Logout: invalida el refresh token actual agregándolo a la lista negra.
    """
    jti = get_jwt()["jti"]  # JWT ID único del token
    BLACKLIST.add(jti)
    return jsonify({"msg": "Refresh token invalidado, logout exitoso"}), 200


# -------------------------------
# Refresh token
# -------------------------------
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    current_user = get_jwt_identity()
    user = User.query.get(current_user)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    new_access_token = create_access_token(
        identity=str(user.id),
        additional_claims={"role": user.role},
    )
    return jsonify({"access_token": new_access_token}), 200

# -------------------------------
# Profile del usuario
# -------------------------------
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404
    return jsonify(user.to_safe_dict()), 200
