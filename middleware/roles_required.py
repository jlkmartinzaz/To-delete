# middleware/roles_required.py
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify

def roles_required(*roles):
    """
    Decorador para proteger rutas basadas en roles.
    - Si no se pasan roles explícitos, se asume 'user' si requiere JWT.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()  # Asegura que haya JWT válido
            claims = get_jwt()
            
            # Si no se pasó rol explícito, asumimos 'user'
            allowed_roles = roles if roles else ("user",)
            
            if claims.get("role") not in allowed_roles:
                return jsonify({"error": "Acceso denegado: rol no autorizado"}), 403
            
            return fn(*args, **kwargs)

        # Guardamos info para inspección
        decorator._roles_required = roles if roles else ("user",)
        decorator._jwt_required = True
        return decorator
    return wrapper
