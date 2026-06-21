import logging

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
logger = logging.getLogger(__name__)
SOURCE_CACHE = "cache"
SOURCE_GITHUB = "github"


@router.get("/user/{username}")
def get_github_user(username: str):
    cache_status = "available"
    try:
        cached_user = CacheHistory().find_by_username(username)
    except Exception:
        logger.exception("No se pudo leer la cache del usuario %s", username)
        cached_user = None
        cache_status = "read_failed"

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
        # Toma los lenguajes de los primeros 7 repos
        # Si falla un repo puntual, continua con los demas sin romper el analisis
        # @autor Esteban
        accumulated_languages = {}
        for repo in repositories[:7]:
            try:
                repo_languages = adapter.get_repository_languages(username, repo["name"])
                for lang, bytes_ in repo_languages.items():
                    accumulated_languages[lang] = accumulated_languages.get(lang, 0) + bytes_
            except GitHubAdapterError:
                continue
        profile_data["languages"] = accumulated_languages
        contributors_per_repo = []
        for repo in repositories[:7]:
            try:
                contributors = adapter.get_repository_contributors(username, repo["name"])
                contributors_per_repo.append({
                    "repository": repo["name"],
                    "contributors": contributors,
                })
            except GitHubAdapterError:
                continue
        profile_data["contributors_per_repo"] = contributors_per_repo


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
    
    profile_dict = _profile_to_dict(profile)
    data_register = DataRegister()
    
    # 1. Guardar en cache JSON (persistencia primaria)
    try:
        data_register.save_user_profile(
            username=profile.username,
            profile=profile_dict,
            analysis=analysis,
        )
    except Exception:
        logger.exception("No se pudo guardar la cache del usuario %s", username)
        cache_status = "write_failed" if cache_status == "available" else "unavailable"
    
    # 2. Persistir en MySQL de forma incremental (no rompe el flujo si falla)
    try:
        db_persisted = data_register.persist_to_mysql(
            username=profile.username,
            profile=profile_dict,
            analysis=analysis,
        )
        if not db_persisted and cache_status == "available":
            cache_status = "db_persist_failed"
    except Exception:
        logger.exception("Error inesperado al persistir en MySQL para %s", username)
        if cache_status == "available":
            cache_status = "db_persist_error"

    metadata = {"source": SOURCE_GITHUB}
    if cache_status != "available":
        metadata["cache"] = cache_status

    return {
        "profile": profile,
        "analysis": analysis,
        "metadata": metadata,
    }


def _profile_to_dict(profile: UserProfile) -> dict:
    """Serializa un perfil manteniendo compatibilidad con Pydantic v1 y v2."""
    if hasattr(profile, "model_dump"):
        return profile.model_dump()

    return profile.dict()


# Endpoints individuales para probar cada analisis de forma independiente
# @autor Esteban

@router.get("/user/{username}/repositories")
def get_user_repositories(username: str):
    adapter = GitHubAdapter()
    try:
        repositories = adapter.get_users_repositories(username)
    except GitHubAdapterError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return {  
        "total_repositories": len(repositories),
        "repositories": repositories,
    }


@router.get("/user/{username}/languages")
def get_user_languages(username: str):
    adapter = GitHubAdapter()
    try:
        repositories = adapter.get_users_repositories(username)
        accumulated_languages = {}
        for repo in repositories[:7]:
            try:
                repo_languages = adapter.get_repository_languages(username, repo["name"])
                for lang, bytes_ in repo_languages.items():
                    accumulated_languages[lang] = accumulated_languages.get(lang, 0) + bytes_
            except GitHubAdapterError:
                continue
        sorted_languages = dict(
            sorted(accumulated_languages.items(), key=lambda x: x[1], reverse=True)
        )
    except GitHubAdapterError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    return {
        "total_languages": len(sorted_languages),
        "primary_language": next(iter(sorted_languages), None),
        "languages": sorted_languages,
    }


@router.get("/user/{username}/contributors")
def get_user_contributors(username: str):
    adapter = GitHubAdapter()
    try:
        repositories = adapter.get_users_repositories(username)
        contributors_per_repo = []
        for repo in repositories[:7]:
            try:
                contributors = adapter.get_repository_contributors(username, repo["name"])
                contributors_per_repo.append({
                    "repository": repo["name"],
                    "contributors": contributors,
                })
            except GitHubAdapterError:
                continue
    except GitHubAdapterError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    unique_contributors = {
        contributor["username"]
        for repo_data in contributors_per_repo
        for contributor in repo_data["contributors"]
    }

    return { 
        "total_contributors": len(unique_contributors),
        "contributors_per_repo": contributors_per_repo,
    }
