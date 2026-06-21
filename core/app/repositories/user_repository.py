from mysql.connector import Error, errorcode

from infrastructure.database import DatabaseConnection


class UsernameAlreadyExistsError(Exception):
    pass


class UserRepository:
    def __init__(self) -> None:
        self._database = DatabaseConnection()

    def find_by_username(self, username: str):
        connection = self._database.get_connection()
        cursor = connection.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = %s",
                (username,),
            )
            return cursor.fetchone()
        finally:
            cursor.close()

    def create(self, username: str, password_hash: str) -> dict:
        connection = self._database.get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (%s, %s)",
                (username, password_hash),
            )
            connection.commit()
            return {"id": cursor.lastrowid, "username": username}
        except Error as exc:
            connection.rollback()
            if exc.errno == errorcode.ER_DUP_ENTRY:
                raise UsernameAlreadyExistsError() from exc
            raise
        finally:
            cursor.close()
