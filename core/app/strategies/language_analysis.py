from typing import Any

from schemas.user_profile import UserProfile
from strategies.interface_analysis import InterfaceAnalysis

# Placeholder para futuras metricas de lenguajes.
# @autor Agus
class LanguageAnalysisStrategy(InterfaceAnalysis):
    @property
    def name(self) -> str:
        return "languages"

    #Toma los lenguajes del router, si no hay lenguajes devuelve un cero para no romper nada. Ordena los lenguajes de mayor a menor segun el codigo que tiene.
    #Suma bytes para calcular porcentajes, si el lenguaje es el primero en la lista(el que tiene mas bytes), muestra una lista ordenada, el lenguaje mas usado, los distintos lenguajes en el repo y por ultimo calcula el porcentaje.
    #Author: Esteban
    def run(self, user_profile: UserProfile) -> dict[str, Any]:
        languages = user_profile.languages

        if not languages:
            return {"languages": {}, "primary_language": None, "total_languages": 0}

        sorted_languages = dict(
            sorted(languages.items(), key=lambda x: x[1], reverse=True)
        )

        total_bytes = sum(languages.values())
        primary_language = next(iter(sorted_languages))

        # Cuenta en cuantos repositorios aparece cada lenguaje
        # Ejemplo: {"Python": 5, "HTML": 3}
        # @autor Esteban
        repos_per_language = {}
        for repo in user_profile.repositories:
            lang = repo.get("language")
            if lang:
                repos_per_language[lang] = repos_per_language.get(lang, 0) + 1

        # Detalle de lenguajes agrupado por repositorio
        # Ejemplo: {"mi-repo": "Python", "otro-repo": "HTML"}
        # @autor Esteban
        languages_per_repo = {
            repo["name"]: repo.get("language")
            for repo in user_profile.repositories
            if repo.get("language")
        }

        return {
            "languages": sorted_languages,
            "primary_language": primary_language,
            "total_languages": len(sorted_languages),
            "percentages": {
                lang: round((bytes_ / total_bytes) * 100, 1)
                for lang, bytes_ in sorted_languages.items()
            },
            # Cantidad de repos donde aparece cada lenguaje
            "repos_per_language": repos_per_language,
            # Lenguaje de cada repositorio
            "languages_per_repo": languages_per_repo,
        }