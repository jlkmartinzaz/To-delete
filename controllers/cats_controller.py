from flask import Blueprint, jsonify
from middleware.roles_required import roles_required

cats_bp = Blueprint("cats_bp", __name__)

@cats_bp.route("/", methods=["GET"])
def list_cats():
    return jsonify({"cats": ["Michi", "Garfield", "Luna"]})

@cats_bp.route("/secret", methods=["GET"])
@roles_required("admin")
def secret_cats():
    return jsonify({"message": "Solo los administradores pueden ver esto 😼"})
