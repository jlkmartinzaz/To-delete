from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from middleware.roles_required import roles_required
from models.cats_model import Cat
from models import db

cats_bp = Blueprint("cats_bp", __name__)

# -------------------------------
# Listar gatos
# -------------------------------
@cats_bp.route("/", methods=["GET"])
@jwt_required()
@roles_required("user", "admin")
def list_cats():
    cats = Cat.query.all()
    return jsonify([cat.to_dict() for cat in cats]), 200


# -------------------------------
# Crear gato
# -------------------------------
@cats_bp.route("/", methods=["POST"])
@jwt_required()
@roles_required("admin")
def create_cat():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    cat = Cat(
        name=name,
        breed=data.get("breed"),
        age=data.get("age"),
        adopted=data.get("adopted", False),
        color=data.get("color"),
        weight=data.get("weight")
    )

    db.session.add(cat)
    db.session.commit()
    return jsonify({"message": "Gato creado correctamente"}), 201


# -------------------------------
# Actualizar gato
# -------------------------------
@cats_bp.route("/<int:cat_id>", methods=["PUT"])
@jwt_required()
@roles_required("admin")
def update_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)
    data = request.get_json() or {}
    cat.name = data.get("name", cat.name)
    cat.breed = data.get("breed", cat.breed)
    cat.age = data.get("age", cat.age)
    cat.adopted = data.get("adopted", cat.adopted)
    cat.color = data.get("color", cat.color)
    cat.weight = data.get("weight", cat.weight)
    db.session.commit()
    return jsonify({"message": "Gato actualizado correctamente"}), 200


# -------------------------------
# Eliminar gato
# -------------------------------
@cats_bp.route("/<int:cat_id>", methods=["DELETE"])
@jwt_required()
@roles_required("admin")
def delete_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    return jsonify({"message": "Gato eliminado correctamente"}), 200
