from sqlalchemy import Column, String, BigInteger, Float, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class FinancialStatement2023(Base):
    __tablename__ = 'financial_statements_2023'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    data = Column(Date)
    reg_ans = Column(String(50), nullable=False)
    cd_conta_contabil = Column(String(50))
    descricao = Column(String(255))
    vl_saldo_inicial = Column(Float)
    vl_saldo_final = Column(Float)

class FinancialStatement2024(Base):
    __tablename__ = 'financial_statements_2024'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    data = Column(Date)
    reg_ans = Column(String(50), nullable=False)
    cd_conta_contabil = Column(String(50))
    descricao = Column(String(255))
    vl_saldo_inicial = Column(Float)
    vl_saldo_final = Column(Float)

class ActiveOperator(Base):
    __tablename__ = 'active_operators'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    registro_ans = Column(String(255), nullable=False)  
    cnpj = Column(String(14))
    razao_social = Column(String(255))
    nome_fantasia = Column(String(255))
    modalidade = Column(String(50))
    logradouro = Column(String(255))
    numero = Column(String(50))
    complemento = Column(String(255))
    bairro = Column(String(255))
    cidade = Column(String(255))
    uf = Column(String(10))
    cep = Column(String(20))
    ddd = Column(String(10))
    telefone = Column(String(30))
    fax = Column(String(30))
    endereco_eletronico = Column(String(255))
    representante = Column(String(255))
    cargo_representante = Column(String(255))
    regiao_de_comercializacao = Column(String(255))
    data_registro_ans = Column(String(255))
