import os
from pathlib import Path

from dotenv import load_dotenv


def _load_env_file() -> None:
    """
    Carga el archivo .env del backend para ejecuciones locales.

    @version 1.0
    @author Agus
    """
    current_file = Path(__file__).resolve()
    env_candidates = [
        current_file.parents[2] / ".env",
        current_file.parents[1] / ".env",
    ]

    for env_file in env_candidates:
        if env_file.exists():
            load_dotenv(env_file)
            return


_load_env_file()


class Settings:
    """
    Centraliza las variables de entorno tecnicas usadas por infraestructura.

    @version 1.0
    @author Agus
    """

    DB_HOST: str = os.getenv("DB_HOST", "database")
    DB_PORT: int = int(os.getenv("DB_PORT", "3306"))
    DB_NAME: str = os.getenv("DB_NAME", "MyGitDB")
    DB_USER: str = os.getenv("DB_USER", "root")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "root")
    GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN")


settings = Settings()
