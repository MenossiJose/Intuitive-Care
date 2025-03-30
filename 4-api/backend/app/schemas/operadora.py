from pydantic import BaseModel
from typing import Optional

class OperadoraNomeCNPJ(BaseModel):
    nome_fantasia: str
    cnpj: str

    class Config:
        from_attributes = True  

class OperadoraDetalhada(BaseModel):
    nome_fantasia: str
    cnpj: str
    modalidade: str
    cidade: str
    uf: str

    class Config:
        from_attributes = True