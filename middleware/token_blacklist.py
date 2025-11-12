# middleware/token_blacklist.py
from datetime import datetime, timedelta
from flask_jwt_extended import get_jwt

# Este diccionario actúa como una "base de datos" temporal para tokens revocados
BLACKLIST = set()

def add_token_to_blacklist(jti):
    """Agrega un token (JTI) a la lista negra."""
    BLACKLIST.add(jti)
    print(f"[{datetime.utcnow()}] Token revocado: {jti}")

def is_token_revoked(jwt_header, jwt_payload):
    """Verifica si el token (JTI) está en la lista negra."""
    jti = jwt_payload.get("jti")
    return jti in BLACKLIST
