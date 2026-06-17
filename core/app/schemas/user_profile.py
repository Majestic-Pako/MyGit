from pydantic import BaseModel
from typing import Any

# Schema interno para representar un perfil de usuario de GitHub.
# Define solo los datos minimos que MyGit va a usar por ahora.
# @autor Agus
class UserProfile(BaseModel):
    username: str
    name: str | None
    avatar_url: str | None
    bio: str | None
    html_url: str
    public_repos: int
    followers: int
    following: int
    account_created_at: str | None
    location: str | None
    company: str | None
    blog: str | None
    twitter_username: str | None
    repositories: list[dict[str, Any]] = [] #Tomamos repositories como list, diccionario, tipo string y any, si no hay retorno, la lista queda vacia para no cometer errores de codigo.
    languages:dict[str,int]={} #Agregamos lenguages #Author: Esteban
    contributors_per_repo: list[dict[str, Any]] = []  # Detalle de colaboradores por repositorio. @autor Esteban
    