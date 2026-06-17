from threading import Lock

import mysql.connector
from mysql.connector import Error

from infrastructure.settings import settings

class DatabaseConnectionError(Exception):
    pass

class DatabaseConnection:

    _instance = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._connection = None

        return cls._instance

    """
        Obtiene una conexion activa a la base de datos MySQL usando la configuracion centralizada.
        @version 1.0
        @author Agus
    """
    def get_connection(self):
        if self._connection and self._connection.is_connected():
            return self._connection

        try:
            self._connection = mysql.connector.connect(
                host=settings.DB_HOST,
                port=settings.DB_PORT,
                database=settings.DB_NAME,
                user=settings.DB_USER,
                password=settings.DB_PASSWORD,
            )
        except Error as exc:
            raise DatabaseConnectionError("No se pudo conectar a la base de datos.") from exc

        return self._connection

    """
        Cierra la conexion activa si existe.
        @version 1.0
        @author Agus
    """
    def close(self) -> None:
        if self._connection and self._connection.is_connected():
            self._connection.close()
