from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

# agregamos la URI de conexión a tu base de datos MongoDB
# cSpell:disable-next-line
MONGO_URI = (
    "mongodb+srv://carlosarturon2020_db_user:"
    "4LgLtY72YQ8BIuVq@fastapi.kenyrka.mongodb.net/"
    "?appName=FastAPI"
)

# Crear una instancia del cliente mongo y asignar tiempo de espera para la
# selección del servidor
client = MongoClient(
    # 15 segundos (antes 3000, muy poco para Atlas)
    MONGO_URI,
    serverSelectionTimeoutMS=15000,
)

# crear la base datos y la coleccion
db = client.amb703
collection = db.trainee

try:
    client.admin.command("ping")  # prueba la conexión
    print("Conexion exitosa a MongoDB")
except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print("Error de conexión a MongoDB:", e)
finally:
    # cerrar la conexión al cliente de MongoDB
    client.close()
