from pydantic import BaseModel

# Schema interno para representar un perfil de usuario de GitHub.
# Define solo los datos minimos que MyGit va a usar por ahora.
# @autor Agus
class UserProfile(BaseModel):
    username: str
    name: str | None
    avatar_url: str | None
    bio: str | None
    public_repos: int
    followers: int
    following: int
    html_url: str
