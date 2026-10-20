from fastapi import APIRouter, HTTPException, Request
from pymongo.database import Database
from pymongo.errors import PyMongoError

router = APIRouter()


@router.get("/health/db")
def database_health(request: Request) -> dict[str, str]:
    database: Database | None = getattr(request.app.state, "database", None)
    if database is None:
        raise HTTPException(
            status_code=503,
            detail="Base de datos no disponible. Define MONGO_URL.",
        )

    try:
        database.command("ping")
    except PyMongoError as exc:
        raise HTTPException(
            status_code=503, detail="No se pudo conectar con MongoDB"
        ) from exc

    return {"status": "ok", "database": "connected"}
