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
        return {}
