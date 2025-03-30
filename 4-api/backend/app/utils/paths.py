from pathlib import Path
import importlib.util
import sys

BASE_DIR = Path(__file__).resolve().parent.parent


MODELS_PATH = BASE_DIR / "models" / "models.py"
SERVICES_PATH = BASE_DIR / "services" / "operadora.py"
API_PATH = BASE_DIR / "api" / "operadoras.py"
SCHEMAS_PATH = BASE_DIR / "schemas" / "operadora.py"
CORE_PATH = BASE_DIR / "core" / "config.py"


def get_models():
    return __import__("app.models.models", fromlist=["*"])

def get_services():
    return __import__("app.services.operadora", fromlist=["*"])

def get_api():
    return __import__("app.api.operadoras", fromlist=["*"])

def get_schemas():
    return __import__("app.schemas.operadora", fromlist=["*"])

def get_core():
    return __import__("app.core.config", fromlist=["*"])

def get_error_handler():
    return __import__("app.utils.handlers", fromlist=["*"])