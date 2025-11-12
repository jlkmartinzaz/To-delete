from flask import Blueprint, request, jsonify
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
    get_jwt
)
from datetime import timedelta
from models.user_model import User
from models import db
from middleware.token_blacklist import add_token_to_blacklist
import json

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

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    # Convertir el identity a cadena JSON para cumplir el estándar JWT
    identity_str = json.dumps({"id": user.id, "role": user.role})

    access_token = create_access_token(
        identity=identity_str,
        expires_delta=timedelta(minutes=2)
    )
    refresh_token = create_refresh_token(
        identity=identity_str,
        expires_delta=timedelta(minutes=5)
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"id": user.id, "email": user.email, "role": user.role}
    }), 200


# -------------------------------
# Logout
# -------------------------------
@auth_bp.route("/logout", methods=["POST"])
@jwt_required(refresh=True)
def logout():
    jti = get_jwt()["jti"]
    add_token_to_blacklist(jti)
    return jsonify({"msg": "Token de refresh invalidado. Logout exitoso."}), 200


# -------------------------------
# Refresh Token
# -------------------------------
@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    # identity llega como string JSON → lo devolvemos igual
    identity_str = get_jwt_identity()
    new_access_token = create_access_token(
        identity=identity_str,
        expires_delta=timedelta(minutes=2)
    )
    return jsonify({"access_token": new_access_token}), 200


# -------------------------------
# Perfil del usuario
# -------------------------------
@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    try:
        identity_data = json.loads(get_jwt_identity())  # decodificamos el string
    except Exception:
        return jsonify({"error": "Token inválido"}), 401

    user = User.query.get(identity_data["id"])
    if not user:
        return jsonify({"error": "Usuario no encontrado"}), 404

    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role
    }), 200
