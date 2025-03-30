from fastapi import HTTPException

class OperadoraNotFoundError(HTTPException):
    def __init__(self, termo: str, search_type: str = "nome"):
        detail = f"Nenhuma operadora encontrada com {search_type}: '{termo}'"
        super().__init__(status_code=404, detail=detail)