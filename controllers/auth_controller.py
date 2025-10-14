from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token, jwt_required

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/test", methods=["GET"])
def test_auth():
    return jsonify({"message": "Auth working!"}), 200

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()

    # Validar datos
    if not data or "email" not in data or "password" not in data:
        return jsonify({"error": "Email and password are required"}), 400

    # Revisar si ya existe el usuario
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"error": "User already exists"}), 409

    # Crear usuario nuevo
    new_user = User(email=data["email"], password=data["password"])
    db.session.add(new_user)
    db.session.commit()

    # Generar token opcional
    access_token = create_access_token(identity=new_user.email)

    return jsonify({
        "message": "User created!",
        "access_token": access_token
    }), 201
