from typing import Any

from schemas.user_profile import UserProfile
from strategies.interface_analysis import InterfaceAnalysis

# Placeholder para futuras metricas de colaboracion.
# @autor Agus
class CollaborationAnalysisStrategy(InterfaceAnalysis):
    @property
    def name(self) -> str:
        return "collaboration"

    def run(self, user_profile: UserProfile) -> dict[str, Any]:
        # Diccionario para acumular datos por colaborador unico
        # @autor Esteban
        contributors_map = {}

        for repo_data in user_profile.contributors_per_repo:
            repo_name = repo_data["repository"]
            for contributor in repo_data["contributors"]:
                username = contributor["username"]

                if username not in contributors_map:
                    # Primera vez que aparece este colaborador
                    contributors_map[username] = {
                        "username": username,
                        "avatar_url": contributor.get("avatar_url"),
                        "html_url": contributor.get("html_url"),
                        "total_contributions": 0,
                        "repositories": [],
                    }

                # Acumula contributions y agrega el repo
                contributors_map[username]["total_contributions"] += contributor.get("contributions", 0)
                contributors_map[username]["repositories"].append(repo_name)

        # Ordena por total de contributions de mayor a menor
        sorted_contributors = sorted(
            contributors_map.values(),
            key=lambda x: x["total_contributions"],
            reverse=True,
        )

        return {
            "total_contributors": len(sorted_contributors),
            "contributors": sorted_contributors,
            "by_repository": user_profile.contributors_per_repo,
        }