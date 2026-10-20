from fastapi import FastAPI, HTTPException

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


# endpoints de la API para la gestión de aprendices
# mensaje de bienvenida a la API
@app.get("/")
async def root():
    return {"message": "API simple con FastApi y  desplegada con RENDER"}


# crear un nuevo aprendiz
@app.post("/trainees", response_description="Crea un nuevo aprendiz")
def crear(trainee: TraineeModel):
    return create_trainee(trainee)


# obtener la lista de aprendices
@app.get("/trainees", response_description="Lista todos los aprendices")
def listar():
    return get_all_trainees()


# obtener un aprendiz por su ID
@app.get(
    "/trainees/{trainee_id}",
    response_description="Obtiene un aprendiz por su ID",
)
def obtener(trainee_id: str):
    if not trainee_id:
        raise HTTPException(
            status_code=404,
            detail="ID de aprendiz no encontrado",
        )
    return get_trainee_by_id(trainee_id)


# actualizar un aprendiz por su ID
@app.put(
    "/trainees/{trainee_id}",
    response_description="Actualiza un aprendiz por su ID",
)
def actualizar(trainee_id: str, trainee: TraineeUpdateModel):
    if not trainee_id:
        raise HTTPException(
            status_code=404,
            detail="ID de aprendiz no encontrado",
        )
    return update_trainee(trainee_id, trainee)


# eliminar un aprendiz por su ID
@app.delete(
    "/trainees/{trainee_id}",
    response_description="Elimina un aprendiz por su ID",
)
def eliminar(trainee_id: str):
    if not trainee_id:
        raise HTTPException(
            status_code=404,
            detail="ID de aprendiz no encontrado",
        )
    return delete_trainee(trainee_id)


# uvicorn src.views.main:app --reload
