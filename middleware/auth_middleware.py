from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt_identity

def role_required(role):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user["role"] != role:
                return jsonify({"msg": "No tienes permisos"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator
