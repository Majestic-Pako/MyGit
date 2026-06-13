from typing import Any

from persistence.cache_settings import USERS_CACHE_FILE
from persistence.json_cache_file import read_json_object


class CacheHistory:
    def __init__(self, cache_file=USERS_CACHE_FILE):
        self.cache_file = cache_file

    def find_by_username(self, username: str) -> dict[str, Any] | None:
        cache_data = read_json_object(self.cache_file)
        cached_profile = cache_data.get(self._normalize_username(username))

        if not self._is_valid_cache_entry(cached_profile):
            return None

        return cached_profile

    def _is_valid_cache_entry(self, cached_profile: Any) -> bool:
        return (
            isinstance(cached_profile, dict)
            and isinstance(cached_profile.get("profile"), dict)
            and isinstance(cached_profile.get("analysis"), dict)
        )

    def _normalize_username(self, username: str) -> str:
        return username.strip().lower()
