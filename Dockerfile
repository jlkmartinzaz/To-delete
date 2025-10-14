# Imagen base ligera
FROM python:3.11-slim

# Directorio de trabajo dentro del contenedor
WORKDIR /src

# Copia todo el contenido del proyecto
COPY . .

# Crea el directorio de base de datos y asigna permisos
RUN mkdir -p /src/data && chmod 777 /src/data

# Instala dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Establece variables de entorno
ENV FLASK_APP=main.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV FLASK_ENV=development

# Expone el puerto Flask
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["flask", "run", "--host=0.0.0.0"]
