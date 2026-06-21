import json

from infrastructure.database import DatabaseConnection


class CacheEntryRepository:
    def __init__(self):
        self.database = DatabaseConnection()

    """
        Persiste una entrada de cache para un perfil de GitHub.
        @version 1.0
        @author Agus
    """
    def save_cache_entry(self, github_profile_id, raw_data_json, expires_at=None, status="active"):
        connection = self.database.get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO cache_entries (
                github_profile_id,
                raw_data_json,
                expires_at,
                status
            )
            VALUES (%s, %s, %s, %s)
        """
        cursor.execute(
            query,
            (
                github_profile_id,
                self._to_json(raw_data_json),
                expires_at,
                status,
            ),
        )
        connection.commit()
        cache_entry_id = cursor.lastrowid
        cursor.close()
        return cache_entry_id

    """
        Obtiene la entrada de cache mas reciente de un perfil.
        @version 1.0
        @author Agus
    """
    def get_latest_by_profile_id(self, github_profile_id):
        connection = self.database.get_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT *
            FROM cache_entries
            WHERE github_profile_id = %s
            ORDER BY created_at DESC
            LIMIT 1
        """
        cursor.execute(query, (github_profile_id,))
        cache_entry = cursor.fetchone()
        cursor.close()
        return cache_entry

    """
        Obtiene y decodifica el ultimo snapshot MySQL de un username.
        @version 1.0
        @author Agus
    """
    def get_latest_snapshot_by_username(self, username):
        connection = self.database.get_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT ce.raw_data_json, ce.created_at
            FROM cache_entries ce
            INNER JOIN github_profiles gp
                ON gp.id = ce.github_profile_id
            WHERE gp.username = %s
            ORDER BY ce.created_at DESC, ce.id DESC
            LIMIT 1
        """
        cursor.execute(query, (username.strip(),))
        cache_entry = cursor.fetchone()
        cursor.close()

        if not cache_entry:
            return None

        raw_data = cache_entry.get("raw_data_json")
        if isinstance(raw_data, (str, bytes, bytearray)):
            try:
                raw_data = json.loads(raw_data)
            except (TypeError, json.JSONDecodeError):
                return None

        if not isinstance(raw_data, dict):
            return None

        return {
            "raw_data": raw_data,
            "created_at": cache_entry.get("created_at"),
        }

    def _to_json(self, raw_data_json):
        if isinstance(raw_data_json, str):
            return raw_data_json

        return json.dumps(raw_data_json, ensure_ascii=False)
