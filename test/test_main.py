from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

import certifi

# URI de conexión a la base de datos MongoDB
MONGO_URI = (
    "mongodb+srv://carlosarturon2020_db_user:4LgLtY72YQ8BIuVq"
    "@fastapi.kenyrka.mongodb.net/?appName=FastAPI"
)


# Crear una instancia del cliente mongo y asignar tiempo de espera #
# para la selección del servidor
client = MongoClient(
    MONGO_URI,
    serverSelectionTimeoutMS=15000,  # 15 segundos
    tlsCAFile=certifi.where(),  # evita errores de certificado SSL
)


# Crear la base de datos y la colección
db = client["amb703"]
collection = db["mesa"]


# Crear el modelo
nueva_mesa = {
    "name": "Carlos Narvaez",
    "status": "Alive",
    "species": "Human",
    "gender": "Male",
}


try:
    client.admin.command("ping")  # prueba la conexión primero
    print("Conexión exitosa a MongoDB")

    # upsert: inserta si no existe, actualiza si ya existe (evita duplicados)
    result = collection.update_one(
        {"name": nueva_mesa["name"]},
        {"$set": nueva_mesa},
        upsert=True,
    )
    if result.upserted_id:
        print("Documento insertado con éxito:", result.upserted_id)
    else:
        print("El documento ya existía, se actualizó.")

    # Opcional: listar las bases de datos para confirmar que todo funciona
    print("Bases de datos:", client.list_database_names())

except (ConnectionFailure, ServerSelectionTimeoutError) as e:
    print("Error de conexión a MongoDB:", e)

except Exception as e:
    # atrapa otros errores (autenticación, DNS, etc.) para ver el mensaje real
    print("Otro error:", type(e).__name__, "-", e)

finally:
    # cerrar la conexión al cliente de MongoDB
    client.close()
