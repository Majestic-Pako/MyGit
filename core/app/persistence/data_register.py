from datetime import datetime, timezone
from typing import Any

from persistence.cache_settings import USERS_CACHE_FILE
from persistence.json_cache_file import read_json_object, write_json_object


class DataRegister:
    def __init__(self, cache_file=USERS_CACHE_FILE):
        self.cache_file = cache_file

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

        try:
            write_json_object(self.cache_file, cache_data)
        except OSError:
            pass

        return cache_data[normalized_username]

    def _normalize_username(self, username: str) -> str:
        return username.strip().lower()

    def _current_timestamp(self) -> str:
        return (
            datetime.now(timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z")
        )
