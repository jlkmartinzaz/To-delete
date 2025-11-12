# middleware/roles_required.py
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify
import json

def roles_required(*roles):
    """
    Decorador para proteger rutas basadas en roles.
    - Si no se pasan roles explícitos, se asume 'user' por defecto.
    - Detecta el rol tanto si está directamente en claims["role"]
      como dentro de claims["sub"] en formato JSON.
    """
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()  # Asegura JWT válido
            claims = get_jwt()

            # Rol permitido por defecto
            allowed_roles = roles if roles else ("user",)

            # Intentamos obtener el rol directamente
            role = claims.get("role")
            
            # Si no está, intentamos extraerlo de "sub" (si es JSON)
            if not role and claims.get("sub"):
                try:
                    sub = json.loads(claims["sub"])
                    role = sub.get("role")
                except Exception:
                    role = None

            if role not in allowed_roles:
                return jsonify({"error": "Acceso denegado: rol no autorizado"}), 403

            return fn(*args, **kwargs)

        # Guardamos info para inspección si se quiere
        decorator._roles_required = roles if roles else ("user",)
        decorator._jwt_required = True
        return decorator
    return wrapper
