# ======================
#   Dockerfile
# ======================
FROM python:3.12-slim

# Evita bytecode y asegura logs visibles
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y build-essential gcc libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente
COPY . .

# Crear carpeta para base de datos y dar permisos
RUN mkdir -p /app/data && chmod -R 777 /app/data

# Exponer puerto interno para Flask (Gunicorn escuchará aquí)
EXPOSE 5000

# Inicializa DB y arranca Gunicorn
CMD ["sh", "-c", "python init_db.py && gunicorn --bind 0.0.0.0:5000 main:create_app"]
