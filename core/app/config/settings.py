import os
from dotenv import load_dotenv

# Carga las variables del archivo .env
load_dotenv()

class Settings:
    PROJECT_NAME: str = "MyGIT Scouting"
    # El token se lee del .env; si no está, queda como None
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")
    
    # Asi agregamos mas configuraciones, por ejemplo:
    API_V1_STR: str = "/api/v1"

settings = Settings()