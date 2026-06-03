import os
from pathlib import Path

from dotenv import load_dotenv

# Carga las variables desde core/.env para ejecuciones locales.
# En Docker, docker-compose tambien inyecta este archivo con env_file.
ENV_FILE = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_FILE)

# Lectura del token guardado si no hay token devuelve null
class Settings:
    PROJECT_NAME: str = "MyGIT Scouting"

    GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN")
    
    API_V1_STR: str = "/api/v1"

settings = Settings()
