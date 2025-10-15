FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y build-essential gcc libpq-dev --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Crear carpeta segura para la base de datos
RUN mkdir -p /app/data && chmod -R 755 /app/data

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
#da




