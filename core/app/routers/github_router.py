from fastapi import APIRouter, HTTPException

from adapters.github_adapter import GitHubAdapter, GitHubAdapterError
from schemas.user_profile import UserProfile
from services.profile_analyzer import ProfileAnalyzer
from strategies.basic_profile_analysis import BasicProfileStrategy
from strategies.collaboration_analysis import CollaborationAnalysisStrategy
from strategies.language_analysis import LanguageAnalysisStrategy

# Router HTTP para endpoints relacionados con GitHub.
# Coordina adapter, schema y estrategias para devolver el perfil analizado.
# @autor Agus
router = APIRouter(prefix="/github", tags=["GitHub"])


@router.get("/user/{username}")
def get_github_user(username: str):
    adapter = GitHubAdapter()
    try:
        profile_data = adapter.get_profile_data(username)
    except GitHubAdapterError as exc:
        raise HTTPException(status_code=exc.status_code, detail=exc.message) from exc

    profile = UserProfile(**profile_data)
    analyzer = ProfileAnalyzer(
        strategies=[
            BasicProfileStrategy(),
            LanguageAnalysisStrategy(),
            CollaborationAnalysisStrategy(),
        ]
    )

    return {
        "profile": profile,
        "analysis": analyzer.run(profile),
    }
