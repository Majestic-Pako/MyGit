from datetime import datetime

from infrastructure.database import DatabaseConnection


class RepositoryRepository:
    def __init__(self):
        self.database = DatabaseConnection()

    """
        Reemplaza y guarda la lista actual de repositorios de un perfil.
        @version 1.0
        @author Agus
    """
    def save_repositories(self, github_profile_id, repositories):
        connection = self.database.get_connection()
        cursor = connection.cursor()
        delete_query = """
            DELETE FROM repositories
            WHERE github_profile_id = %s
        """
        insert_query = """
            INSERT INTO repositories (
                github_profile_id,
                name,
                description,
                language,
                stargazers_count,
                forks_count,
                repo_created_at,
                last_activity_at,
                html_url
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(delete_query, (github_profile_id,))
        if not repositories:
            connection.commit()
            cursor.close()
            return 0

        cursor.executemany(
            insert_query,
            [self._repository_values(github_profile_id, repository) for repository in repositories],
        )
        connection.commit()
        saved_count = cursor.rowcount
        cursor.close()
        return saved_count

    def _repository_values(self, github_profile_id, repository):
        return (
            github_profile_id,
            repository.get("name"),
            repository.get("description"),
            repository.get("language"),
            repository.get("stargazers_count", 0),
            repository.get("forks_count", 0),
            self._parse_datetime(repository.get("created_at")),
            self._parse_datetime(repository.get("last_commit")),
            repository.get("html_url"),
        )

    def _parse_datetime(self, value):
        if not value:
            return None

        if isinstance(value, datetime):
            return value

        return datetime.fromisoformat(value.replace("Z", "+00:00")).replace(tzinfo=None)
