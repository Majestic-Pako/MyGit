from pydantic import BaseModel

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
