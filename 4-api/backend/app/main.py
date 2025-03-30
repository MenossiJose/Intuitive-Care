from fastapi import FastAPI
from app.utils.paths import get_api

# Get the module
operadoras = get_api()

app = FastAPI(title="API de Operadoras")

app.include_router(operadoras.router, prefix="/api")