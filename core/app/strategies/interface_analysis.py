from abc import ABC, abstractmethod
from typing import Any

from schemas.user_profile import UserProfile

# Interfaz base para estrategias de analisis de perfiles.
# Cada estrategia recibe un UserProfile y devuelve su resultado.
# @autor Agus
class InterfaceAnalysis(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def run(self, user_profile: UserProfile) -> dict[str, Any]:
        pass
