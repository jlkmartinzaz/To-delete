from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from middleware.roles_required import roles_required
from models.cats_model import Cat
from models import db

cats_bp = Blueprint("cats_bp", __name__)

@cats_bp.route("/", methods=["GET"])
@roles_required("user")  # 🔹 agregamos rol explícito
@jwt_required()
def list_cats():
    cats = Cat.query.all()
    return jsonify([cat.to_dict() for cat in cats]), 200

@cats_bp.route("/", methods=["POST"])
@roles_required("admin")
def create_cat():
    data = request.get_json() or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "El nombre es obligatorio"}), 400

    cat = Cat(name=name, breed=data.get("breed"), age=data.get("age"), adopted=data.get("adopted", False))
    db.session.add(cat)
    db.session.commit()
    return jsonify({"message": "Gato creado correctamente"}), 201

@cats_bp.route("/<int:cat_id>", methods=["PUT"])
@roles_required("admin")
def update_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)
    data = request.get_json() or {}
    cat.name = data.get("name", cat.name)
    cat.breed = data.get("breed", cat.breed)
    cat.age = data.get("age", cat.age)
    cat.adopted = data.get("adopted", cat.adopted)
    db.session.commit()
    return jsonify({"message": "Gato actualizado correctamente"}), 200

@cats_bp.route("/<int:cat_id>", methods=["DELETE"])
@roles_required("admin")
def delete_cat(cat_id):
    cat = Cat.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    return jsonify({"message": "Gato eliminado correctamente"}), 200
