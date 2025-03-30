from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.utils.paths import get_core, get_services, get_schemas, get_error_handler


core = get_core()
services = get_services()
schemas = get_schemas()
error_handler = get_error_handler()

router = APIRouter()

def get_db():
    db = core.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/buscar_nome", response_model=list[schemas.OperadoraNomeCNPJ])
def buscar_nome(termo: str, db: Session = Depends(get_db)):
    results = services.buscar_operadoras(db, termo)
    return error_handler.check_empty_results(results, termo, "nome")

@router.get("/buscar_detalhada_nome", response_model=list[schemas.OperadoraDetalhada])
def buscar_detalhada_nome(termo: str, db: Session = Depends(get_db)):
    results = services.buscar_operadoras(db, termo)
    return error_handler.check_empty_results(results, termo, "nome")

@router.get("/buscar_cnpj", response_model=list[schemas.OperadoraNomeCNPJ])
def buscar_cnpj(termo: str, db: Session = Depends(get_db)):
    results = services.buscar_operadoras_cnpj(db, termo)
    return error_handler.check_empty_results(results, termo, "CNPJ")

@router.get("/buscar_detalhada_cnpj", response_model=list[schemas.OperadoraDetalhada])
def buscar_detalhada_cnpj(termo: str, db: Session = Depends(get_db)):
    results = services.buscar_operadoras_cnpj(db, termo)
    return error_handler.check_empty_results(results, termo, "CNPJ")

@router.get("/buscar_razao_social", response_model=list[schemas.OperadoraDetalhada])
def buscar_razao_social(termo: str, db: Session = Depends(get_db)):
    results = services.buscar_operadoras_razao_social(db, termo)
    return error_handler.check_empty_results(results, termo, "razao_social")

@router.get("/buscar_cidade_uf", response_model=list[schemas.OperadoraDetalhada])
def buscar_cidade_uf(cidade: str, uf: str, db: Session = Depends(get_db)):
    results = services.buscar_operadoras_cidade_uf(db, cidade, uf)
    return error_handler.check_empty_results(results, f"{cidade} / {uf}", "cidade e uf")

@router.get("/buscar_modalidade", response_model=list[schemas.OperadoraDetalhada])
def buscar_modalidade(termo: str, db: Session = Depends(get_db)):
    results = services.buscar_operadoras_modalidade(db, termo)
    return error_handler.check_empty_results(results, termo, "modalidade")