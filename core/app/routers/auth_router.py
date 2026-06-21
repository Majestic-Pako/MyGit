from fastapi import APIRouter, HTTPException, status
from mysql.connector import Error
from pydantic import BaseModel

from infrastructure.database import DatabaseConnectionError
from repositories.user_repository import UserRepository, UsernameAlreadyExistsError
from services.password_hasher import hash_password, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])
user_repository = UserRepository()


class AuthRequest(BaseModel):
    username: str
    password: str


class AuthResponse(BaseModel):
    id: int
    username: str


def clean_credentials(credentials: AuthRequest) -> tuple[str, str]:
    username = credentials.username.strip()
    password = credentials.password

    if not username or not password.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El usuario y la contraseña son obligatorios.",
        )

    return username, password


@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
def register(credentials: AuthRequest):
    username, password = clean_credentials(credentials)

    try:
        if user_repository.find_by_username(username):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El nombre de usuario ya existe.",
            )

        return user_repository.create(username, hash_password(password))
    except UsernameAlreadyExistsError as exc:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="El nombre de usuario ya existe.",
        ) from exc
    except (DatabaseConnectionError, Error) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo acceder a la base de datos.",
        ) from exc


@router.post("/login", response_model=AuthResponse)
def login(credentials: AuthRequest):
    username, password = clean_credentials(credentials)

    try:
        user = user_repository.find_by_username(username)
    except (DatabaseConnectionError, Error) as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo acceder a la base de datos.",
        ) from exc

    if not user or not verify_password(password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos.",
        )

    return {"id": user["id"], "username": user["username"]}
