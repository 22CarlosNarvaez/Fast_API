# API y consola de aprendices

API REST con FastAPI y MongoDB. La consola usa `requests` para llamar todas las
rutas: inicio, estado de la base de datos y operaciones CRUD de aprendices.

## Configuración

Instala las dependencias y configura la URI de MongoDB como variable de entorno:

```bash
python3 -m pip install -r requirements.txt
export MONGO_URL='mongodb+srv://usuario:contraseña@cluster.mongodb.net/'
```

Opcionalmente, puedes definir `MONGO_DB_NAME` (predeterminado `amb703`) y
`MONGO_COLLECTION_NAME` (predeterminado `trainee`). La consola apunta por
defecto a `https://fast-api-97xd.onrender.com`; para consumir una instancia
local, configura `API_BASE_URL=http://127.0.0.1:8000`.

## Ejecutar

En una terminal, inicia la API:

```bash
uvicorn src.views.main:app --reload
```

En otra terminal, abre la consola interactiva:

```bash
python3 -m src.views.views
```

El menú incluye `GET /`, `GET /health/db`, `GET /trainees`, `POST /trainees`,
`GET /trainees/{trainee_id}`, `PUT /trainees/{trainee_id}` y
`DELETE /trainees/{trainee_id}`. La documentación interactiva de FastAPI está
disponible en `http://127.0.0.1:8000/docs`.

Sin `MONGO_URL`, la API puede iniciar, pero los endpoints de base de datos
responden con HTTP 503 y un mensaje de configuración.

## Pruebas

Las pruebas de la consola no realizan llamadas reales a la API ni acceden a
MongoDB:

```bash
python3 -m unittest discover -s test -v
```