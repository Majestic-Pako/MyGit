from infrastructure.settings import settings as env_settings


"""
    Define la configuracion general de la aplicacion FastAPI.

    @version 1.0
    @author Agus
"""
class Settings:
    PROJECT_NAME: str = "MyGIT Scouting"
    GITHUB_TOKEN: str | None = env_settings.GITHUB_TOKEN
    
    API_V1_STR: str = "/api/v1"

settings = Settings()
