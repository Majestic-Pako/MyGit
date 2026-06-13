from pathlib import Path

CACHE_ROOT = Path(__file__).resolve().parents[2] / "storage" / "cache"
USERS_CACHE_FILE = CACHE_ROOT / "users_cache.json"
