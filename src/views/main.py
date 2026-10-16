from src.templates.controllers import (
    create_trainee,
    get_all_trainees,
    get_trainee_by_id,
    update_trainee,
    delete_trainee,
)


from src.models.model import TraineeModel, TraineeUpdateModel # noqa: F401
from fastapi import FastAPI, HTTPException, status # noqa: F401

app = FastAPI(
    title="Gestión de datos de los aprendices",
    description="API simple con FastAPI para consumir"
    "los datos de los aprendicez",
    version="1.0.0",
)

# uvicorn  src.main:app --reload
