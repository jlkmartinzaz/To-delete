# Introducción

Este proyecto consiste en una API desarrollada con Flask para la gestión
de usuarios y registros de gatos. Cuenta con autenticación basada en
JWT, roles de usuario (`user` y `admin`), y operaciones CRUD sobre los
registros de gatos. El proyecto está dockerizado para facilitar su
despliegue y prueba.

# Rutas y Roles

  **Método**   **Ruta**         **JWT requerido**   **Roles permitidos**
  ------------ ---------------- ------------------- ----------------------
  **Método**   **Ruta**         **JWT requerido**   **Roles permitidos**
  POST         /auth/register   No                  None
  POST         /auth/login      No                  None
  POST         /auth/logout     No                  None
  POST         /auth/refresh    Sí                  user
  GET          /auth/profile    Sí                  user
  GET          /cats/           Sí                  user
  POST         /cats/           Sí                  admin
  PUT          /cats/\<id\>     Sí                  admin
  DELETE       /cats/\<id\>     Sí                  admin

# Configuración y Dependencias

## Archivo `requirements.txt`

``` {.bash language="bash"}
Flask
        Flask-JWT-Extended
        Flask-SQLAlchemy
        python-dotenv
```

## Instalación de dependencias

``` {.bash language="bash"}
pip install -r requirements.txt
```

# Docker

## Dockerfile

``` {.bash language="bash"}
FROM python:3.12-slim
        
        WORKDIR /app
        
        COPY requirements.txt .
        RUN pip install --no-cache-dir -r requirements.txt
        
        COPY . .
        
        EXPOSE 5000
        
        CMD ["python", "app.py"]
```

## docker-compose.yml

``` {.bash language="bash"}
version: '3.9'
        services:
        api:
        build: .
        ports:
        - "5000:5000"
        volumes:
        - .:/app
        environment:
        - FLASK_ENV=development
```

## Ejecutar con Docker

1.  Construir la imagen:

    ``` {.bash language="bash"}
    docker-compose build
    ```

2.  Levantar el contenedor:

    ``` {.bash language="bash"}
    docker-compose up
    ```

3.  Acceder a la API en `http://localhost:5000`

# Ejecutar Pruebas Automáticas

Para probar la API de manera automatizada se incluye el script
`test_api.sh`. Este script realiza:

-   Registro de usuario.

-   Login y obtención de JWT.

-   Refresh token.

-   Operaciones CRUD sobre gatos según el rol.

## Ejecutar el script

``` {.bash language="bash"}
bash test_api.sh
```

# Conclusión

Esta API demuestra la implementación de autenticación JWT, control de
roles y operaciones CRUD en Flask. El proyecto está dockerizado para
facilitar despliegue y pruebas, y la documentación incluye rutas, roles
y ejemplos de uso. El script de prueba permite validar automáticamente
la funcionalidad de la API en un entorno local.
