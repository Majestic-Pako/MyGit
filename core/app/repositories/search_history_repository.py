from infrastructure.database import DatabaseConnection


class SearchHistoryRepository:
    def __init__(self):
        self.database = DatabaseConnection()

    """
        Guarda un registro simple del historial de busqueda.
        @version 1.0
        @author Agus
    """
    def save_search_history(self, user_id, github_profile_id, source="api", status="success"):
        connection = self.database.get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO search_history (
                user_id,
                github_profile_id,
                source,
                status
            )
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(query, (user_id, github_profile_id, source, status))
        connection.commit()
        search_history_id = cursor.lastrowid
        cursor.close()
        return search_history_id
