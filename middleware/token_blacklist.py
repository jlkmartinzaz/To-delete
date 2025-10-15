# middleware/token_blocklist.py
from flask_jwt_extended import get_jwt
from models import db  # si quieres guardar blacklist en DB
from flask import jsonify

# Lista negra en memoria (para pruebas)
BLACKLIST = set()

def add_token_to_blacklist(jti):
    BLACKLIST.add(jti)

def is_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in BLACKLIST
