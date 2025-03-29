import time
import mysql.connector  # Mudança aqui
from etl.loader import load_csv_data, load_list_data

# Configuração do banco de dados (MySQL no Docker)
DB_HOST = "localhost"
DB_PORT = 3306  # Mudança para a porta padrão do MySQL
DB_USER = "ansUser"
DB_PASSWORD = "ansPassword"
DB_NAME = "ansDb"

# Arquivos de entrada
list_files = [
    "data/raw/4T2024.csv",
    "data/raw/3T2024.csv",
    "data/raw/2T2024.csv",
    "data/raw/1T2024.csv",
    "data/raw/4T2023.csv",
    "data/raw/3T2023.csv",
    "data/raw/2T2023.csv",
    "data/raw/1T2023.csv",
]
file_path = "data/raw/Relatorio_cadop.csv"

# Queries de inserção conforme o schema definido em sql/schema.sql
query_active_operators = """
INSERT INTO active_operators 
(registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

query_financial_statements_2023 = """
INSERT INTO financial_statements_2023 
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
VALUES (%s, %s, %s, %s, %s, %s)
"""

query_financial_statements_2024 = """
INSERT INTO financial_statements_2024 
(data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
VALUES (%s, %s, %s, %s, %s, %s)
"""

# Mapeamento para identificar qual query utilizar, de acordo com o ano presente no nome do arquivo
queries = {
    "2023": query_financial_statements_2023,
    "2024": query_financial_statements_2024
}

def run_schema(conn, schema_file="sql/schemas.sql"):
    """Executa o script SQL para criação das tabelas."""
    with open(schema_file, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    with conn.cursor() as cur:
        for statement in schema_sql.split(";"):  # Divide comandos SQL se houver múltiplos
            if statement.strip():
                cur.execute(statement)
    conn.commit()
    print("Schema criado com sucesso.")

def main():
    initial_time = time.time()

    # Conecta ao MySQL (rodando em Docker)
    conn = mysql.connector.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )
    
    # Cria as tabelas conforme o schema
    run_schema(conn)
    
    # Carrega os dados do arquivo de operadoras (tabela active_operators)
    load_csv_data(conn, file_path, query_active_operators, batch_size=20000)
    
    # Carrega os dados dos arquivos de demonstrativos (tabelas financial_statements_2023/2024)
    load_list_data(conn, list_files, queries, batch_size=20000)
    
    conn.close()
    print(f"Tempo de execução: {time.time() - initial_time:.2f} segundos")

if __name__ == "__main__":
    main()
