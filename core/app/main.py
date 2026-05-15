from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"HOLA MUNDO :)" " ESTO ES UNA PRUEBA DE DESPLIEGUE EN DOCKER"}
