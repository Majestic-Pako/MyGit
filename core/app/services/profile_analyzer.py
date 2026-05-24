from typing import Any

from schemas.user_profile import UserProfile
from strategies.base_strategy import AnalysisStrategy

# Servicio orquestador de estrategias de analisis.
# Ejecuta las estrategias registradas sobre un perfil interno.
# @autor Agus


class ProfileAnalyzer:
    def __init__(self, strategies: list[AnalysisStrategy]):
        self.strategies = strategies

    def run(self, user_profile: UserProfile) -> dict[str, dict[str, Any]]:
        results = {}

        for strategy in self.strategies:
            strategy_name = strategy.__class__.__name__
            results[strategy_name] = strategy.run(user_profile)

        return results
