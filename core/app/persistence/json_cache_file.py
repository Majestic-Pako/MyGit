import json
from pathlib import Path
from typing import Any


def read_json_object(file_path: Path) -> dict[str, Any]:
    try:
        if not file_path.exists() or file_path.stat().st_size == 0:
            return {}

        with file_path.open("r", encoding="utf-8") as cache_file:
            data = json.load(cache_file)
    except (OSError, json.JSONDecodeError):
        return {}

    if not isinstance(data, dict):
        return {}

    return data


def write_json_object(file_path: Path, data: dict[str, Any]) -> None:
    file_path.parent.mkdir(parents=True, exist_ok=True)
    temp_file = file_path.with_suffix(f"{file_path.suffix}.tmp")

    with temp_file.open("w", encoding="utf-8") as cache_file:
        json.dump(data, cache_file, ensure_ascii=False, indent=2)
        cache_file.write("\n")

    temp_file.replace(file_path)
