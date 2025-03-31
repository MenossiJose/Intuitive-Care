from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.utils.paths import get_api

# Get the module
operadoras = get_api()

app = FastAPI(title="API de Operadoras")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(operadoras.router, prefix="/api")