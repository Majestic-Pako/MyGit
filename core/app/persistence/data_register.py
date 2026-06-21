import json
import logging
from datetime import datetime, timezone
from typing import Any

from persistence.cache_settings import USERS_CACHE_FILE
from persistence.json_cache_file import read_json_object, write_json_object
from infrastructure.database import DatabaseConnection, DatabaseConnectionError

logger = logging.getLogger(__name__)


class DataRegister:
    # Inicializa el registrador con el archivo JSON de cache.
    # @version 2.0
    # @author Agus
    def __init__(self, cache_file=USERS_CACHE_FILE):
        self.cache_file = cache_file
        self.db = DatabaseConnection()

    # Guarda profile y analysis en cache bajo el username normalizado.
    # Mantiene compatibilidad con versión anterior.
    # @version 1.0
    # @author Agus
    def save_user_profile(
        self,
        username: str,
        profile: dict[str, Any],
        analysis: dict[str, Any],
    ) -> dict[str, Any]:
        cache_data = read_json_object(self.cache_file)
        cached_at = self._current_timestamp()
        normalized_username = self._normalize_username(username)

        cache_data[normalized_username] = {
            "cached_at": cached_at,
            "profile": profile,
            "analysis": analysis,
        }

        write_json_object(self.cache_file, cache_data)

        return cache_data[normalized_username]

    # Persiste el perfil y análisis en MySQL de forma transacional.
    # Si falla, no propaga la excepción para mantener funcional el cache JSON.
    # @version 1.0
    # @author Agus
    def persist_to_mysql(
        self,
        username: str,
        profile: dict[str, Any],
        analysis: dict[str, Any],
    ) -> bool:
        """
        Persiste datos en MySQL de forma incremental.

        Retorna True si el guardado fue exitoso, False en caso de error.
        Los errores se loguean pero no se propagan para mantener
        funcional el flujo del cache JSON.
        """
        connection = None
        cursor = None

        try:
            connection = self.db.get_connection()
            cursor = connection.cursor()

            # Inicia transacción
            cursor.execute("START TRANSACTION")

            # 1. Crear o obtener github_profile
            profile_id = self._upsert_github_profile(cursor, username, profile)

            # 2. Limpiar datos anteriores del perfil
            self._clean_profile_data(cursor, profile_id)

            # 3. Insertar repositories
            repositories_saved = self._insert_repositories(cursor, profile_id, profile)

            # 4. Insertar languages
            languages_saved = self._insert_languages(cursor, profile_id, analysis)

            # 5. Insertar collaborators
            collaborators_saved = self._insert_collaborators(cursor, profile_id, profile)

            # 6. Actualizar profile_metrics
            self._upsert_profile_metrics(cursor, profile_id, profile, analysis)

            # 7. Guardar raw_data en cache_entries
            raw_data = {
                "profile": profile,
                "analysis": analysis,
                "timestamp": self._current_timestamp(),
            }
            self._insert_cache_entry(cursor, profile_id, raw_data)

            # Confirmar transacción
            connection.commit()
            logger.info(
                "Perfil %s persistido en MySQL: %s repositorios, %s lenguajes, %s colaboradores",
                username,
                repositories_saved,
                languages_saved,
                collaborators_saved,
            )
            return True

        except DatabaseConnectionError as exc:
            logger.error("Error de conexión a MySQL para %s: %s", username, exc)
            return False
        except Exception as exc:
            logger.error("Error al persistir %s en MySQL: %s", username, exc)
            try:
                if connection is not None:
                    connection.rollback()
            except Exception:
                pass
            return False
        finally:
            try:
                if cursor is not None:
                    cursor.close()
            except Exception:
                pass

    def _upsert_github_profile(
        self, cursor: Any, username: str, profile: dict[str, Any]
    ) -> int:
        """Crea o actualiza el registro en github_profiles y retorna su ID."""
        query = """
        INSERT INTO github_profiles
        (username, first_name, last_name, biography, image_profile,
         followers, following, public_repos, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
        ON DUPLICATE KEY UPDATE
            first_name = VALUES(first_name),
            last_name = VALUES(last_name),
            biography = VALUES(biography),
            image_profile = VALUES(image_profile),
            followers = VALUES(followers),
            following = VALUES(following),
            public_repos = VALUES(public_repos),
            updated_at = NOW()
        """

        first_name = profile.get("name", "").split()[0] if profile.get("name") else None
        last_name = profile.get("name", "").split()[-1] if profile.get("name") else None

        cursor.execute(
            query,
            (
                username,
                first_name,
                last_name,
                profile.get("bio"),
                profile.get("avatar_url"),
                profile.get("followers", 0),
                profile.get("following", 0),
                profile.get("public_repos", 0),
            ),
        )

        # Obtener el ID del perfil
        query_select = "SELECT id FROM github_profiles WHERE username = %s"
        cursor.execute(query_select, (username,))
        result = cursor.fetchone()

        return result[0] if result else None

    def _clean_profile_data(self, cursor: Any, profile_id: int) -> None:
        """Limpia datos anteriores asociados al perfil."""
        cursor.execute("DELETE FROM repositories WHERE github_profile_id = %s", (profile_id,))
        cursor.execute("DELETE FROM languages WHERE github_profile_id = %s", (profile_id,))
        cursor.execute("DELETE FROM collaborators WHERE github_profile_id = %s", (profile_id,))

    def _insert_repositories(
        self, cursor: Any, profile_id: int, profile: dict[str, Any]
    ) -> int:
        """Inserta repositories del perfil."""
        repositories = profile.get("repositories", [])

        if not repositories:
            return 0

        query = """
        INSERT INTO repositories
        (github_profile_id, name, description, language, stargazers_count,
         forks_count, repo_created_at, last_activity_at, html_url)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        for repo in repositories:
            cursor.execute(
                query,
                (
                    profile_id,
                    repo.get("name"),
                    repo.get("description"),
                    repo.get("language"),
                    repo.get("stargazers_count", 0),
                    repo.get("forks_count", 0),
                    self._normalize_mysql_datetime(repo.get("created_at")),
                    self._normalize_mysql_datetime(
                        repo.get("last_commit") or repo.get("pushed_at")
                    ),
                    repo.get("html_url"),
                ),
            )

        return len(repositories)

    def _insert_languages(
        self, cursor: Any, profile_id: int, analysis: dict[str, Any]
    ) -> int:
        """Inserta languages del análisis."""
        languages_data = analysis.get("languages", {})
        languages = languages_data.get("languages", {})
        percentages = languages_data.get("percentages", {})
        repositories_per_language = languages_data.get("repos_per_language", {})

        if not languages:
            return 0

        query = """
        INSERT INTO languages
        (github_profile_id, name, percentage, bytes_count, repositories_count)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            percentage = VALUES(percentage),
            bytes_count = VALUES(bytes_count),
            repositories_count = VALUES(repositories_count)
        """

        for lang, bytes_count in languages.items():
            percentage = percentages.get(lang, 0)
            repositories_count = repositories_per_language.get(lang, 0)
            cursor.execute(
                query,
                (profile_id, lang, percentage, bytes_count, repositories_count),
            )

        return len(languages)

    def _insert_collaborators(
        self, cursor: Any, profile_id: int, profile: dict[str, Any]
    ) -> int:
        """Inserta collaborators del perfil."""
        contributors_per_repo = profile.get("contributors_per_repo", [])

        if not contributors_per_repo:
            return 0

        query = """
        INSERT INTO collaborators
        (github_profile_id, username, avatar_url, html_url, contributions)
        VALUES (%s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
            avatar_url = VALUES(avatar_url),
            html_url = VALUES(html_url),
            contributions = VALUES(contributions)
        """

        collaborators = {}

        for repo_data in contributors_per_repo:
            for contributor in repo_data.get("contributors", []):
                username = contributor.get("username") or contributor.get("login")
                if not username:
                    continue

                collaborator = collaborators.setdefault(
                    username,
                    {
                        "avatar_url": contributor.get("avatar_url"),
                        "html_url": contributor.get("html_url"),
                        "contributions": 0,
                    },
                )
                collaborator["contributions"] += contributor.get("contributions", 0) or 0

        for username, collaborator in collaborators.items():
            cursor.execute(
                query,
                (
                    profile_id,
                    username,
                    collaborator.get("avatar_url"),
                    collaborator.get("html_url"),
                    collaborator.get("contributions", 0),
                ),
            )

        return len(collaborators)

    def _upsert_profile_metrics(
        self,
        cursor: Any,
        profile_id: int,
        profile: dict[str, Any],
        analysis: dict[str, Any],
    ) -> None:
        """Crea o actualiza las métricas del perfil."""
        languages_data = analysis.get("languages", {})
        primary_language = languages_data.get("primary_language")
        collaboration_data = analysis.get("collaboration", {})

        repositories = profile.get("repositories", [])
        repositories_with_activity = [
            (
                repository,
                self._normalize_mysql_datetime(
                    repository.get("last_commit") or repository.get("pushed_at")
                ),
            )
            for repository in repositories
        ]
        repositories_with_activity = [
            item for item in repositories_with_activity if item[1] is not None
        ]
        most_active_repo = (
            max(repositories_with_activity, key=lambda item: item[1])[0].get("name")
            if repositories_with_activity
            else None
        )
        total_collaborators = collaboration_data.get("total_contributors")
        if total_collaborators is None:
            total_collaborators = len(
                {
                    contributor.get("username") or contributor.get("login")
                    for repo in profile.get("contributors_per_repo", [])
                    for contributor in repo.get("contributors", [])
                    if contributor.get("username") or contributor.get("login")
                }
            )
        total_commits = 0

        query = """
        INSERT INTO profile_metrics
        (github_profile_id, total_repositories, total_commits, total_collaborators,
         most_used_language, most_active_repository, last_update)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
        ON DUPLICATE KEY UPDATE
            total_repositories = VALUES(total_repositories),
            total_commits = VALUES(total_commits),
            total_collaborators = VALUES(total_collaborators),
            most_used_language = VALUES(most_used_language),
            most_active_repository = VALUES(most_active_repository),
            last_update = NOW()
        """

        cursor.execute(
            query,
            (
                profile_id,
                len(repositories),
                total_commits,
                total_collaborators,
                primary_language,
                most_active_repo,
            ),
        )

    def _insert_cache_entry(
        self, cursor: Any, profile_id: int, raw_data: dict[str, Any]
    ) -> None:
        """Inserta el raw_data completo en cache_entries."""
        query = """
        INSERT INTO cache_entries
        (github_profile_id, raw_data_json, created_at, status)
        VALUES (%s, %s, NOW(), 'active')
        """

        raw_data_json = json.dumps(raw_data, ensure_ascii=False, indent=2)
        cursor.execute(query, (profile_id, raw_data_json))

    # Normaliza el username para mantener una sola clave por usuario.
    # @version 1.0
    # @author Agus
    def _normalize_username(self, username: str) -> str:
        return username.strip().lower()

    def _normalize_mysql_datetime(self, value: Any) -> datetime | None:
        """Convierte fechas ISO de GitHub a DATETIME UTC sin zona horaria."""
        if value is None or value == "":
            return None

        if isinstance(value, datetime):
            parsed_date = value
        elif isinstance(value, str):
            try:
                parsed_date = datetime.fromisoformat(value.strip().replace("Z", "+00:00"))
            except ValueError:
                logger.warning("Fecha de GitHub invalida, se guardara NULL: %s", value)
                return None
        else:
            logger.warning("Tipo de fecha de GitHub no soportado: %s", type(value).__name__)
            return None

        if parsed_date.tzinfo is not None:
            parsed_date = parsed_date.astimezone(timezone.utc).replace(tzinfo=None)

        return parsed_date

    # Genera la fecha UTC del registro cacheado en formato ISO.
    # @version 1.0
    # @author Agus
    def _current_timestamp(self) -> str:
        return (
            datetime.now(timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )
