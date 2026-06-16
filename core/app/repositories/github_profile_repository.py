from infrastructure.database import DatabaseConnection


class GitHubProfileRepository:
    def __init__(self):
        self.database = DatabaseConnection()

    """
        Busca un perfil de GitHub por nombre de usuario.
        @version 1.0
        @author Agus
    """
    def find_by_username(self, username):
        connection = self.database.get_connection()
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT *
            FROM github_profiles
            WHERE username = %s
            LIMIT 1
        """
        cursor.execute(query, (username,))
        profile = cursor.fetchone()
        cursor.close()
        return profile

    """
        Crea o actualiza un perfil de GitHub y devuelve su id.
        @version 1.0
        @author Agus
    """
    def create_or_update(self, profile_data):
        connection = self.database.get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO github_profiles (
                username,
                first_name,
                last_name,
                biography,
                image_profile,
                followers,
                following,
                public_repos
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                id = LAST_INSERT_ID(id),
                first_name = VALUES(first_name),
                last_name = VALUES(last_name),
                biography = VALUES(biography),
                image_profile = VALUES(image_profile),
                followers = VALUES(followers),
                following = VALUES(following),
                public_repos = VALUES(public_repos)
        """
        cursor.execute(query, self._profile_values(profile_data))
        connection.commit()
        profile_id = cursor.lastrowid
        cursor.close()
        return profile_id

    def _profile_values(self, profile_data):
        first_name, last_name = self._split_name(profile_data.get("name"))
        return (
            profile_data.get("username"),
            first_name,
            last_name,
            profile_data.get("bio"),
            profile_data.get("avatar_url"),
            profile_data.get("followers", 0),
            profile_data.get("following", 0),
            profile_data.get("public_repos", 0),
        )

    def _split_name(self, full_name):
        if not full_name:
            return None, None

        parts = full_name.split(maxsplit=1)
        first_name = parts[0]
        last_name = parts[1] if len(parts) > 1 else None
        return first_name, last_name
