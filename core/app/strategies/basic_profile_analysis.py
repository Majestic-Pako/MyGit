from typing import Any

from schemas.user_profile import UserProfile
from strategies.interface_analysis import InterfaceAnalysis

# Estrategia inicial para exponer metricas basicas del perfil.
# Sirve como base simple para agregar analisis mas avanzados despues.
# @autor Agus
class BasicProfileStrategy(InterfaceAnalysis):
    @property
    def name(self) -> str:
        return "basic_profile"

    def run(self, user_profile: UserProfile) -> dict[str, Any]:
        return {
            "username": user_profile.username,
            "name": user_profile.name,
            "bio": user_profile.bio,
            "avatar_url": user_profile.avatar_url,
            "html_url": user_profile.html_url,
            "public_repos": user_profile.public_repos,
            "followers": user_profile.followers,
            "following": user_profile.following,
            "account_created_at": user_profile.account_created_at,
            "location": user_profile.location,
            "company": user_profile.company,
            "blog": user_profile.blog,
            "twitter_username": user_profile.twitter_username,
        }
