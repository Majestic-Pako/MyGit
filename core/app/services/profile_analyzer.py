from typing import Any

from schemas.user_profile import UserProfile
from strategies.interface_analysis import InterfaceAnalysis

# Servicio orquestador de estrategias de analisis.
# Ejecuta las estrategias registradas sobre un perfil interno.
# @autor Agus
class ProfileAnalyzer:
    def __init__(self, strategies: list[InterfaceAnalysis]):
        self.strategies = strategies

    def run(self, user_profile: UserProfile) -> dict[str, dict[str, Any]]:
        results = {}

        for strategy in self.strategies:
            results[strategy.name] = strategy.run(user_profile)

        return results
