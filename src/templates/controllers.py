from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException
from pymongo.errors import PyMongoError

from src.models.database import collection
from src.models.model import TraineeModel, TraineeUpdateModel


def helper_trainee(trainee: dict) -> dict[str, str | int]:
    return {
        "id": str(trainee["_id"]),
        "document": trainee["document"],
        "firstname": trainee["firstname"],
        "lastname": trainee["lastname"],
        "email": trainee["email"],
        "age": trainee["age"],
        "program": trainee["program"],
        "record_number": trainee["record_number"],
    }


def _get_collection():
    if collection is None:
        raise HTTPException(
            status_code=503,
            detail="MongoDB no está configurado. Define MONGO_URL.",
        )
    return collection


def _get_object_id(trainee_id: str) -> ObjectId:
    try:
        return ObjectId(trainee_id)
    except (InvalidId, TypeError) as exc:
        raise HTTPException(
            status_code=404,
            detail="ID de aprendiz no válido",
        ) from exc


def _database_error() -> HTTPException:
    return HTTPException(
        status_code=503,
        detail="No se pudo completar la operación en MongoDB",
    )


def create_trainee(trainee: TraineeModel) -> dict:
    try:
        trainee_collection = _get_collection()
        result = trainee_collection.insert_one(trainee.model_dump())
        new_trainee = trainee_collection.find_one({"_id": result.inserted_id})
    except PyMongoError as exc:
        raise _database_error() from exc

    if new_trainee is None:
        raise HTTPException(
            status_code=500,
            detail="No se pudo recuperar el aprendiz creado",
        )
    return helper_trainee(new_trainee)


def get_all_trainees() -> list[dict]:
    try:
        return [
            helper_trainee(trainee)
            for trainee in _get_collection().find()
        ]
    except PyMongoError as exc:
        raise _database_error() from exc


def get_trainee_by_id(trainee_id: str) -> dict:
    try:
        trainee = _get_collection().find_one(
            {"_id": _get_object_id(trainee_id)}
        )
    except PyMongoError as exc:
        raise _database_error() from exc

    if trainee is None:
        raise HTTPException(status_code=404, detail="Aprendiz no encontrado")
    return helper_trainee(trainee)


def update_trainee(trainee_id: str, data: TraineeUpdateModel) -> dict:
    data_update = data.model_dump(exclude_unset=True, exclude_none=True)
    if not data_update:
        raise HTTPException(
            status_code=400,
            detail="Debes enviar al menos un campo para actualizar",
        )

    try:
        trainee_collection = _get_collection()
        result = trainee_collection.update_one(
            {"_id": _get_object_id(trainee_id)},
            {"$set": data_update},
        )
        if result.matched_count == 0:
            raise HTTPException(
                status_code=404,
                detail="Aprendiz no encontrado",
            )
        trainee_updated = trainee_collection.find_one(
            {"_id": _get_object_id(trainee_id)}
        )
    except PyMongoError as exc:
        raise _database_error() from exc

    if trainee_updated is None:
        raise HTTPException(
            status_code=404,
            detail="Aprendiz no encontrado",
        )
    return helper_trainee(trainee_updated)


def delete_trainee(trainee_id: str) -> bool:
    try:
        result = _get_collection().delete_one(
            {"_id": _get_object_id(trainee_id)}
        )
    except PyMongoError as exc:
        raise _database_error() from exc

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Aprendiz no encontrado")
    return True
