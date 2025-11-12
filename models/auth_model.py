from datetime import datetime
from models.user_model import User
from middleware.token_blacklist import add_token_to_blacklist
from flask_jwt_extended import create_access_token, create_refresh_token

def register_user(db, email, password, role="user"):
    """
    Registra un nuevo usuario.
    """
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return {"message": "El usuario ya existe."}, 400

    user = User(email=email)
    user.set_password(password)
    user.role = role
    db.session.add(user)
    db.session.commit()
    return {"message": "Usuario registrado exitosamente."}, 201


def login_user(email, password):
    """
    Inicia sesión y devuelve tokens JWT.
    """
    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return {"message": "Credenciales inválidas."}, 401

    access_token = create_access_token(identity={"id": user.id, "role": user.role})
    refresh_token = create_refresh_token(identity={"id": user.id, "role": user.role})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": {"email": user.email, "role": user.role}
    }, 200


def logout_user(jti):
    """
    Revoca el token actual agregándolo a la lista negra.
    """
    add_token_to_blacklist(jti)
    return {"message": "Sesión cerrada correctamente."}, 200
