from fastapi import APIRouter, HTTPException

from adapters.github_adapter import GitHubAdapter, GitHubAdapterError
from schemas.user_profile import UserProfile
from services.profile_analyzer import ProfileAnalyzer
from strategies.basic_profile_analysis import BasicProfileStrategy
from strategies.collaboration_analysis import CollaborationAnalysisStrategy
from strategies.language_analysis import LanguageAnalysisStrategy
from strategies.repository_analysis import RepositoryAnalysisStrategy #Empieza desde la carpeta strategies y importa el archivo necesario. @Autor Esteban
#Se agrego esto, nada mas.
from adapters.github_adapter import(GitHubAdapter,GitHubAdapter,GitHubAdapterError,GitHubAdapter,GitHubAdapterError,GitHubAPIError,GitHubNotFoundError,GitHubRateLimitError,GitHubUnauthorizedError,GitHubConnectionError,)
# Router HTTP para endpoints relacionados con GitHub.
# Coordina adapter, schema y estrategias para devolver el perfil analizado.
# @autor Agus
router = APIRouter(prefix="/github", tags=["GitHub"])


@router.get("/user/{username}")
def get_github_user(username: str):
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

    return {
        "profile": profile,
        "analysis": analyzer.run(profile),
    }
