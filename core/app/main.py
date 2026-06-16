from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.db_router import router as db_router
from routers.github_router import router as github_router

# Punto de entrada de la API FastAPI.
# Registra los routers disponibles del backend.
# @autor Agus

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(github_router)
app.include_router(db_router)


@app.get("/")
def home():
    return {"message": "HOLA MUNDO :) ESTO ES UNA PRUEBA DE DESPLIEGUE EN DOCKER"}
