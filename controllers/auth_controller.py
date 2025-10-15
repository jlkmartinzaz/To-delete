# controllers/auth_controller.py
from flask import Blueprint, request, jsonify
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

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Credenciales inválidas"}), 401

    access_token = create_access_token(
        identity=user.id,
        additional_claims={"role": user.role},
    )
    refresh_token = create_refresh_token(identity=user.id)

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user.to_safe_dict()
    }), 200

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
        identity=user.id,
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


