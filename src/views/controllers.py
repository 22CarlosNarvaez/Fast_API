from bson import ObjectId # noqa: F401
from src.models.database import collection
from src.models.model import TraineeModel, TraineeUpdateModel # noqa: F401


def helper_trainee(trainee) -> dict:
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


def create_trainee(trainee: TraineeModel):
    trainee_dict = trainee.model_dump()
    result = collection.insert_one(trainee_dict)
    new_trainee = collection.find_one({"_id": result.inserted_id})
    return helper_trainee(new_trainee)
