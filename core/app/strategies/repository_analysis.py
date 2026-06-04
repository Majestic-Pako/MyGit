from typing import Any

from schemas.user_profile import UserProfile
from strategies.interface_analysis import InterfaceAnalysis


# Placeholder para futuras metricas de repositorios.
# @autor Agus
class RepositoryAnalysisStrategy(InterfaceAnalysis):

    @property
    def name(self) -> str:
        return "repositories"

    def run(self, user_profile: UserProfile) -> dict[str, Any]:

        repositories = user_profile.repositories

        most_starred = max(
            repositories,
            key=lambda repo: repo["stargazers_count"],
            default=None
        )

        most_forked = max(
            repositories,
            key=lambda repo: repo["forks_count"],
            default=None
        )

        recently_updated = sorted(
        repositories,
        key=lambda repo: repo["last_commit"] or "",
        reverse=True
        )[:5]

        languages = list({
            repo["language"]
            for repo in repositories
            if repo["language"]
        })

        return {
            "total_repositories": len(repositories),
            "most_starred": most_starred,
            "most_forked": most_forked,
            "recently_updated": recently_updated,
            "languages": languages,
        }