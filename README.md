# API FastAPI conectada a MongoDB

La conexión está centralizada en `src/database.py`. Al iniciar, FastAPI carga
`.env`, crea el cliente de MongoDB y verifica la conexión con `ping`. La base y
colección predeterminadas conservan los nombres del proyecto: `amb703.mesa`.

## Configuración

Define la URI en el `.env` existente, sin escribir credenciales en el código:

```env
MONGO_URL=mongodb+srv://usuario:contraseña@cluster.mongodb.net/?appName=FastAPI
```

Si tu base o colección tienen otros nombres, puedes configurarlos así:

```env
MONGO_DB_NAME=amb703
MONGO_COLLECTION_NAME=mesa
```

En MongoDB Atlas, confirma que el usuario tenga permisos para la base y que la
IP desde la que ejecutas la aplicación esté permitida en Network Access.

## Instalar y ejecutar

```bash
pip install -r requirements.txt
uvicorn src.main:app --reload
```

La ruta `GET /health/db` devuelve el estado de la conexión. Las pruebas se
ejecutan sin acceder a MongoDB:

```bash
python -m unittest discover -s test
```