from fastapi import FastAPI

from src.models.model import TraineeModel, TraineeUpdateModel
from src.templates.controllers import (
    create_trainee,
    delete_trainee,
    get_all_trainees,
    get_trainee_by_id,
    update_trainee,
)

app = FastAPI(
    title="Gestión de datos de los aprendices",
    description="API simple con FastAPI para consumir "
    "los datos de los aprendices",
    version="1.0.0",
)


@app.post("/trainees")
def crear(trainee: TraineeModel):
    return create_trainee(trainee)


@app.get("/trainees")
def listar():
    return get_all_trainees()


@app.get("/trainees/{trainee_id}")
def obtener(trainee_id: str):
    return get_trainee_by_id(trainee_id)


@app.put("/trainees/{trainee_id}")
def actualizar(trainee_id: str, trainee: TraineeUpdateModel):
    return update_trainee(trainee_id, trainee)


@app.delete("/trainees/{trainee_id}")
def eliminar(trainee_id: str):
    return delete_trainee(trainee_id)

# uvicorn src.views.main:app --reload
