import os
from sqlalchemy import create_engine, func, desc, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models.models import FinancialStatement2023, FinancialStatement2024, ActiveOperator

# Load environment variables
load_dotenv()

# Database connection
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_USER = os.getenv("DB_USER", "ansUser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "ansPassword")
DB_NAME = os.getenv("DB_NAME", "ansDb")

# Create SQLAlchemy engine
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=False)
Session = sessionmaker(bind=engine)

def top_10_operators_last_quarter():
    """
    Query the top 10 operators with highest expenses in
    "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"
    in the last quarter.
    """
    session = Session()
    
    query = text("""
    SELECT DISTINCT ao.registro_ans, ao.razao_social, SUM(fs.vl_saldo_final) AS total_expense
    FROM financial_statements_2024 fs
    JOIN (
        SELECT DISTINCT registro_ans, razao_social 
        FROM active_operators
    ) ao ON fs.reg_ans = ao.registro_ans
    WHERE fs.data = '2024-10-01'  -- Last quarter date
    AND fs.descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%SAÚDE MEDICO HOSPITALAR%'
    GROUP BY ao.registro_ans, ao.razao_social
    ORDER BY total_expense DESC
    LIMIT 10
    """)
    
    results = session.execute(query).fetchall()
    session.close()
    
    print("Top 10 Operators with Highest Expenses (Last Quarter):")
    for idx, row in enumerate(results, 1):
        print(f"{idx}. {row.razao_social}: R$ {row.total_expense:,.2f}")
    
    return results

def top_10_operators_last_year():
    """
    Query the top 10 operators with highest expenses in
    "EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR"
    in the last year.
    """
    session = Session()
    
    query = text("""
    WITH last_year_data AS (
        SELECT reg_ans, SUM(vl_saldo_final) AS total_expense
        FROM (
            SELECT reg_ans, vl_saldo_final 
            FROM financial_statements_2024
            WHERE descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%SAÚDE MEDICO HOSPITALAR%'
            UNION ALL
            SELECT reg_ans, vl_saldo_final 
            FROM financial_statements_2023
            WHERE descricao LIKE '%EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS%SAÚDE MEDICO HOSPITALAR%'
        ) combined
        GROUP BY reg_ans
    )
    SELECT DISTINCT ao.registro_ans, ao.razao_social, lyd.total_expense
    FROM last_year_data lyd
    JOIN (
        SELECT DISTINCT registro_ans, razao_social
        FROM active_operators
    ) ao ON lyd.reg_ans = ao.registro_ans
    ORDER BY lyd.total_expense DESC
    LIMIT 10
    """)
    
    results = session.execute(query).fetchall()
    session.close()
    
    print("\nTop 10 Operators with Highest Expenses (Last Year):")
    for idx, row in enumerate(results, 1):
        print(f"{idx}. {row.razao_social}: R$ {row.total_expense:,.2f}")
    
    return results

if __name__ == "__main__":
    print("Running top operators analytics queries...\n")
    top_10_operators_last_quarter()
    top_10_operators_last_year()
    print("\nAnalysis complete!")