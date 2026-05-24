from typing import Any

from schemas.user_profile import UserProfile
from strategies.interface_analysis import InterfaceAnalysis

# Placeholder para futuras metricas de lenguajes.
# @autor Agus
class LanguageAnalysisStrategy(InterfaceAnalysis):
    @property
    def name(self) -> str:
        return "languages"

    def run(self, user_profile: UserProfile) -> dict[str, Any]:
        return {}
