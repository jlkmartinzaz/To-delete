#!/usr/bin/env bash
set -e

# cargar .env si existe
if [ -f .env ]; then
  export $(cat .env | sed 's/#.*//g' | xargs)
fi

# inicializar db (SQLite crea archivo)
python - <<'PY'
from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()
print("DB initialized (if not existing).")
PY

exec "$@"
