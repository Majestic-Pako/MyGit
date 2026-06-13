from typing import Any

from persistence.cache_settings import USERS_CACHE_FILE
from persistence.json_cache_file import read_json_object


class CacheHistory:
    # Inicializa el historial de cache con el archivo JSON de usuarios.
    # @version 1.0
    # @author Agus
    def __init__(self, cache_file=USERS_CACHE_FILE):
        self.cache_file = cache_file

    # Busca un usuario en cache usando el username normalizado.
    # @version 1.0
    # @author Agus
    def find_by_username(self, username: str) -> dict[str, Any] | None:
        cache_data = read_json_object(self.cache_file)
        cached_profile = cache_data.get(self._normalize_username(username))

        if not self._is_valid_cache_entry(cached_profile):
            return None

        return cached_profile

    # Valida que la entrada cacheada tenga profile y analysis.
    # @version 1.0
    # @author Agus
    def _is_valid_cache_entry(self, cached_profile: Any) -> bool:
        return (
            isinstance(cached_profile, dict)
            and isinstance(cached_profile.get("profile"), dict)
            and isinstance(cached_profile.get("analysis"), dict)
        )

    # Normaliza el username para evitar duplicados por mayusculas.
    # @version 1.0
    # @author Agus
    def _normalize_username(self, username: str) -> str:
        return username.strip().lower()
