from fastapi import FastAPI

from routers.github_router import router as github_router

# Punto de entrada de la API FastAPI.
# Registra los routers disponibles del backend.
# @autor Agus

app = FastAPI()

app.include_router(github_router)


@app.get("/")
def home():
    return {"message": "HOLA MUNDO :) ESTO ES UNA PRUEBA DE DESPLIEGUE EN DOCKER"}
