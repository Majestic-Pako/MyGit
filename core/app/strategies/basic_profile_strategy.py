from typing import Any

from schemas.user_profile import UserProfile
from strategies.base_strategy import AnalysisStrategy

# Estrategia inicial para exponer metricas basicas del perfil.
# Sirve como base simple para agregar analisis mas avanzados despues.
# @autor Agus
class BasicProfileStrategy(AnalysisStrategy):
    def run(self, user_profile: UserProfile) -> dict[str, Any]:
        return {
            "username": user_profile.username,
            "public_repos": user_profile.public_repos,
            "followers": user_profile.followers,
            "following": user_profile.following,
        }
