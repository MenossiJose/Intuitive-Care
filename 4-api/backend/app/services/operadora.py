from sqlalchemy.orm import Session
from app.utils.paths import get_models

models = get_models()

def buscar_operadoras(db: Session, termo: str):
    return db.query(models.ActiveOperator).filter(models.ActiveOperator.nome_fantasia.like(f"%{termo}%")).all()

def buscar_operadoras_cnpj(db: Session, termo: str):
    return db.query(models.ActiveOperator).filter(models.ActiveOperator.cnpj.like(f"%{termo}%")).all()


def buscar_operadoras_razao_social(db: Session, termo: str):
    return db.query(models.ActiveOperator)\
             .filter(models.ActiveOperator.razao_social.like(f"%{termo}%"))\
             .all()

def buscar_operadoras_cidade_uf(db: Session, cidade: str, uf: str):
    return db.query(models.ActiveOperator)\
             .filter(
                 models.ActiveOperator.cidade.like(f"%{cidade}%"),
                 models.ActiveOperator.uf.like(f"%{uf}%")
             )\
             .all()

def buscar_operadoras_modalidade(db: Session, termo: str):
    return db.query(models.ActiveOperator)\
             .filter(models.ActiveOperator.modalidade.like(f"%{termo}%"))\
             .all()