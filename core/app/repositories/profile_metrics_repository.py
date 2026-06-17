from infrastructure.database import DatabaseConnection


class ProfileMetricsRepository:
    def __init__(self):
        self.database = DatabaseConnection()

    """
        Persiste las metricas de un perfil y devuelve el id del registro.
        @version 1.0
        @author Agus
    """
    def create_or_update(self, github_profile_id, metrics_data):
        connection = self.database.get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO profile_metrics (
                github_profile_id,
                total_repositories,
                total_commits,
                total_collaborators,
                most_used_language,
                most_active_repository
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                id = LAST_INSERT_ID(id),
                total_repositories = VALUES(total_repositories),
                total_commits = VALUES(total_commits),
                total_collaborators = VALUES(total_collaborators),
                most_used_language = VALUES(most_used_language),
                most_active_repository = VALUES(most_active_repository),
                last_update = CURRENT_TIMESTAMP
        """
        cursor.execute(
            query,
            (
                github_profile_id,
                metrics_data.get("total_repositories", 0),
                metrics_data.get("total_commits", 0),
                metrics_data.get("total_collaborators", 0),
                metrics_data.get("most_used_language"),
                metrics_data.get("most_active_repository"),
            ),
        )
        connection.commit()
        metrics_id = cursor.lastrowid
        cursor.close()
        return metrics_id
