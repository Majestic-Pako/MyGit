from typing import Any

import httpx

from config.settings import settings

# Adapter para consumir la API publica de GitHub.
# Convierte la respuesta externa en un formato interno propio.
# @autor Agus
class GitHubAdapterError(Exception):
    def __init__(self, message: str, status_code: int = 502):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

#Se agrega el excepciones propias para el proyecto basadas en clases.
#Mas abajo(o otra parte..) se agrega el manejo de excepciones.
#Autor: Esteban
class GitHubAPIError(GitHubAdapterError):
    """Error generico de la API de GitHub."""

class GitHubNotFoundError(GitHubAdapterError):
    """Usuario o recurso no encontrado (404)."""

class GitHubRateLimitError(GitHubAdapterError):
    """Rate limit alcanzado (403 / 429)."""

class GitHubUnauthorizedError(GitHubAdapterError):
    """Token invalido o sin permisos (401)."""

class GitHubConnectionError(GitHubAdapterError):
    """No se pudo establecer conexion con GitHub."""

class GitHubAdapter:
    BASE_URL = "https://api.github.com"

    def __init__(self, timeout: float = 10.0):
        self.timeout = timeout

    def _github_token(self) -> str | None:
        token = settings.GITHUB_TOKEN
        if not token:
            return None

        token = token.strip().strip('"').strip("'")
        if token in {"tu_token_aqui", "tu_token_de_github"}:
            return None

        return token

    def _headers(self) -> dict[str, str]:
        headers = {
            "Accept": "application/vnd.github+json",
            "User-Agent": "MyGit-FastAPI",
        }

        token = self._github_token()
        if token:
            auth_scheme = "token" if token.startswith("ghp_") else "Bearer"
            headers["Authorization"] = f"{auth_scheme} {token}"

        return headers
    #Manejo de Excepciones, aca abajo.
    #Author: Esteban
    def _handle_response_errors(self, response: httpx.Response, context: str) -> None:
        code = response.status_code

        if code == 401 or code == 403:
            if code == 403 and "rate limit" in response.text.lower():
                raise GitHubRateLimitError(
                    "Rate limit de GitHub alcanzado. Intenta de nuevo en unos minutos.",
                    status_code=429,
                )
            raise GitHubUnauthorizedError(
                "Token de GitHub invalido o sin permisos necesarios.",
                status_code=401,
            )

        if code == 404:
            raise GitHubNotFoundError(
                f"No se encontro el {context} en GitHub.",
                status_code=404,
            )

        if code == 429:
            raise GitHubRateLimitError(
                "Rate limit de GitHub alcanzado. Intenta de nuevo en unos minutos.",
                status_code=429,
            )

        if code >= 500:
            raise GitHubAPIError(
                "GitHub respondio con un error de servidor. Intenta mas tarde.",
                status_code=502,
            )

        if code >= 400:
            raise GitHubAPIError(
                f"Error inesperado al obtener {context}.",
                status_code=500,
            )
    def get_profile_data(self, username: str) -> dict[str, Any]:
        url = f"{self.BASE_URL}/users/{username}"

        try:
            response = httpx.get(url, headers=self._headers(), timeout=self.timeout)
        except httpx.RequestError as exc:
            raise GitHubAdapterError("GitHub no responde en este momento.") from exc

        if response.status_code == 404:
            raise GitHubAdapterError("Usuario de GitHub no encontrado.", status_code=404)

        if response.status_code == 401:
            raise GitHubAdapterError("Token de GitHub invalido o vencido. Revisa GITHUB_TOKEN en core/.env.", status_code=401)

        if response.status_code >= 400:
            raise GitHubAdapterError(f"No se pudo obtener el perfil desde GitHub. Status {response.status_code}")

        data = response.json()
        return self._map_profile_data(data)

    def _map_profile_data(self, data: dict[str, Any]) -> dict[str, Any]:
        return {
            "username": data["login"],
            "name": data.get("name"),
            "avatar_url": data.get("avatar_url"),
            "bio": data.get("bio"),
            "html_url": data["html_url"],
            "public_repos": data.get("public_repos", 0),
            "followers": data.get("followers", 0),
            "following": data.get("following", 0),
            "account_created_at": data.get("created_at"),
            "location": data.get("location"),
            "company": data.get("company"),
            "blog": data.get("blog"),
            "twitter_username": data.get("twitter_username"),
        }
    # Define y toma la variable asignada con la base de URL propuesto 
    # Retorna las descripciones mencionadas pedidas.
    #Hace un bucle para cada uno y llama a JSON.
    #@autor Esteban
    def get_users_repositories(self, username: str) -> list[dict[str, Any]]:
        url = f"{self.BASE_URL}/users/{username}/repos"

        response = httpx.get(
            url,
            headers=self._headers(),
            params={"sort": "updated", "per_page": 30},
            timeout=self.timeout,
        )

        if response.status_code == 404:
            raise GitHubAdapterError("Usuario de GitHub no encontrado.", status_code=404)

        if response.status_code == 401:
            raise GitHubAdapterError("Token de GitHub invalido o vencido. Revisa GITHUB_TOKEN en core/.env.", status_code=401)

        if response.status_code >= 400:
            raise GitHubAdapterError(f"No se pudieron obtener los repositorios desde GitHub. Status {response.status_code}")

        return [
            #Retorna lo indicado de abajo y se agrego fecha de creacion y ultimo commit que seria la fecha del ultimo commit.
            #@autor: Esteban.
        {
            "name": repo["name"],
            "description": repo.get("description"),
            "language": repo.get("language"),
            "stargazers_count": repo.get("stargazers_count", 0),
            "forks_count": repo.get("forks_count", 0),
            "created_at": repo.get("created_at"),
            "last_commit": repo.get("pushed_at"),
            "html_url": repo["html_url"],   
        }
        for repo in response.json()   
    ]
    def get_repository_languages(self, owner: str, repo: str) -> dict[str, int]:
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/languages"

        try:
            response = httpx.get(url, headers=self._headers(), timeout=self.timeout)
        except httpx.RequestError as exc:
            raise GitHubConnectionError("GitHub no responde en este momento.") from exc

        if response.status_code != 200 or not response.content:
            return {}

        try:
            languages_data = response.json()
        except ValueError:
            return {}

        if not isinstance(languages_data, dict):
            return {}

        return languages_data  # {"Python": 12400, "HTML": 3200, ...}

    def get_repository_contributors(self, owner: str, repo: str) -> list[dict[str, Any]]:
        url = f"{self.BASE_URL}/repos/{owner}/{repo}/contributors"

        try:
            response = httpx.get(url, headers=self._headers(), timeout=self.timeout)
        except httpx.RequestError as exc:
            raise GitHubConnectionError("GitHub no responde en este momento.") from exc

        if response.status_code != 200 or not response.content:
            return []

        try:
            contributors_data = response.json()
        except ValueError:
            return []

        if not isinstance(contributors_data, list):
            return []

        return [
            {
                "username": contributor["login"],
                "avatar_url": contributor.get("avatar_url"),
                "html_url": contributor.get("html_url"),
                "contributions": contributor.get("contributions", 0),
            }
            for contributor in contributors_data
            if isinstance(contributor, dict) and contributor.get("login")
        ]
