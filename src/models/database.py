import os

import certifi
from pymongo import MongoClient
from pymongo.database import Database

MONGO_URI = os.getenv("mongodb+srv://carlosarturon2020_db_user:"
                      "4LgLtY72YQ8BIuVq@fastapi.kenyrka.mongodb.net/"
                      "?appName=FastAPI")

client: MongoClient | None = None
database: Database | None = None
collection = None

if MONGO_URI:
    client = MongoClient(
        MONGO_URI,
        serverSelectionTimeoutMS=5000,
        tlsCAFile=certifi.where(),
    )
    database = client[os.getenv("MONGO_DB_NAME", "amb703")]
    collection = database[os.getenv("MONGO_COLLECTION_NAME", "trainee")]
