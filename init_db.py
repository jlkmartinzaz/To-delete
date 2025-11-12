# init_db.py
from app import create_app
from models import db

app = create_app()

with app.app_context():
    print("Verificando base de datos...")
    db.create_all()
    print("Tablas creadas (si no existían).")
