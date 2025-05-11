# Death Note API 📓

Una API RESTful basada en FastAPI inspirada en Death Note, permitiendo gestionar y manipular información relacionada con el universo de Death Note. En donde se podra registar a las personas y especificar su muerte, esto siguiendo las siguientes reglas:

- Solo podran morir las personas registradas con una imagen.
- Despues de registar a la persona tendra 40 seg para registar la causa de la muerte.
- Si no se especifica la causa de la muerte, esta morira por un ataque al corazon.
- Si la causa de la muerte es especificada, se tienen 6 minutos y 40 segundos adicionales para escribir los detalles específicos. En este caso, la persona morirá 40 seg después de especificar los detalles.

## 🚀 Características

- CRUD completo para gestión de personas en la death note
- Integración con Firebase para almacenamiento de datos
- Soporte para subida de imágenes usando Cloudinary
- Documentación automática con Swagger UI
- Manejo de errores HTTP personalizado
- Soporte para CORS

## 📋 Pre-requisitos

- Python 3.11 o superior
- Cuenta en Firebase
- Cuenta en Cloudinary
- Docker (opcional)

## 🔧 Variables de Entorno

Crear un archivo `.env` en la raíz del proyecto con las siguientes variables:

```env
FIRE_BASE_KEY=
APY_KEY=
AUTH_DOMAIN=
PROJECT_ID=
STORAGE_BUCKET=
MESSAGING_SENDER_ID=
APP_ID=
MEASUREMENT_ID=
DATABASE_URL=""

CLOUDINARY_CLOUD_NAME=
CLOUDINARY_API_KEY=
CLOUDINARY_API_SECRET=
CLOUDINARY_URL=
```

## 🛠️ Instalación

1. Clonar el repositorio
```bash
git clone https://github.com/AC-Santiago/DeathNoteFakeAPI.git
cd DeathNoteFakeAPI
```

2. Crear y activar entorno virtual


- Con uv:
```bash
uv sync
source .venv/bin/activate # Linux/Mac
.\.venv\Scripts\activate # Windows
```


## 🐳 Uso con Docker

1. Construir la imagen y ejecutarla

```bash
docker compose up --build
```



## 🚀 Ejecutar sin Docker

```bash
fastapi run app/main.py --host 0.0.0.0 --port 8000
```

La API estará disponible en `http://localhost:8000`

## 📖 Documentación

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 🛣️ Endpoints

- `GET /personas`: Obtiene lista de personas
- `POST /personas`: Crea una nueva persona
- `POST /personas/death`: Programa la muerte de la persona especificada

## 🛠️ Construido con

- [FastAPI](https://fastapi.tiangolo.com/) - Framework web moderno y rápido
- [Firebase Admin SDK](https://firebase.google.com/docs/admin/setup) - Base de datos y autenticación
- [Cloudinary](https://cloudinary.com/) - Gestión de imágenes en la nube
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Validación de datos
- [Docker](https://www.docker.com/) - Containerización

## ✒️ Autor

* **Santiago Acosta Cespedes** - *Desarrollo de la Api* - [AC-Santiago](https://github.com/AC-Santiago)

### Colaboradores

* **Sebastian Alejandro Mojica Lozada** - *Colaborador* - [Sebastianmjk](https://github.com/Sebastianmjk)
* **Julio Cesar Contreras Granda** - *Colaborador* - [Juliocontreras03](https://github.com/Juliocontreras03)
* **Santiago Antonio Neira** - *Colaborador* - [Santiago-Neira](https://github.com/Santiago-Neira)


## 📄 Licencia

Este proyecto está bajo la Licencia  GPL-3.0 license  - mira el archivo [LICENSE](LICENSE) para detalles
