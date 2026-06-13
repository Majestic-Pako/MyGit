from fastapi import APIRouter, HTTPException

from adapters.github_adapter import GitHubAdapter, GitHubAdapterError
from persistence.cache_history import CacheHistory
from persistence.data_register import DataRegister
from schemas.user_profile import UserProfile
from services.profile_analyzer import ProfileAnalyzer
from strategies.basic_profile_analysis import BasicProfileStrategy
from strategies.collaboration_analysis import CollaborationAnalysisStrategy
from strategies.language_analysis import LanguageAnalysisStrategy
from strategies.repository_analysis import RepositoryAnalysisStrategy #Empieza desde la carpeta strategies y importa el archivo necesario. @Autor Esteban

# Router HTTP para endpoints relacionados con GitHub.
# Coordina adapter, schema y estrategias para devolver el perfil analizado.
# @autor Agus
router = APIRouter(prefix="/github", tags=["GitHub"])
SOURCE_CACHE = "cache"
SOURCE_GITHUB = "github"


@router.get("/user/{username}")
def get_github_user(username: str):
    cache_history = CacheHistory()
    cached_user = cache_history.find_by_username(username)

    if cached_user:
        return {
            "profile": cached_user.get("profile", {}),
            "analysis": cached_user.get("analysis", {}),
            "metadata": {
                "source": SOURCE_CACHE,
                "cached_at": cached_user.get("cached_at"),
            },
        }

    adapter = GitHubAdapter()
    try:
        profile_data = adapter.get_profile_data(username)
        
        repositories = adapter.get_users_repositories(username) #Declara la variable y llama desde adapter a la otra variable asignada que es get_users_repositories.@Autor Esteban
        profile_data["repositories"] = repositories #Toma profile_data, toma clave repositories y guarda la lista de repositorios.@Autor Esteban
    except GitHubAdapterError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    profile = UserProfile(**profile_data)
    analyzer = ProfileAnalyzer(
        strategies=[
            BasicProfileStrategy(),
            LanguageAnalysisStrategy(),
            CollaborationAnalysisStrategy(),
            RepositoryAnalysisStrategy(), #LLamamos al archivo asignado. @Autor Esteban
        ]
    )
    analysis = analyzer.run(profile)
    DataRegister().save_user_profile(
        username=profile.username,
        profile=_profile_to_dict(profile),
        analysis=analysis,
    )

    return {
        "profile": profile,
        "analysis": analysis,
        "metadata": {
            "source": SOURCE_GITHUB,
        },
    }


# Convierte el UserProfile a dict manteniendo compatibilidad de Pydantic.
# @version 1.0
# @author Agus
def _profile_to_dict(profile: UserProfile) -> dict:
    if hasattr(profile, "model_dump"):
        return profile.model_dump()

    return profile.dict()
