from fastapi import APIRouter, HTTPException
from mysql.connector import Error

from infrastructure.database import DatabaseConnection, DatabaseConnectionError
from infrastructure.settings import settings


router = APIRouter(prefix="/db", tags=["Database"])


@router.get("/health")

def database_health():
    """
    Verifica que la API pueda conectarse a MySQL sin exponer datos sensibles.
    pd. no me dejaba ponerlo arriba :,v
    @version 1.0
    @author Agus
    """
    try:
        connection = DatabaseConnection().get_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
    except (DatabaseConnectionError, Error) as exc:
        raise HTTPException(
            status_code=503,
            detail="No se pudo conectar a la base de datos.",
        ) from exc

    return {
        "database": "connected",
        "name": settings.DB_NAME,
    }
