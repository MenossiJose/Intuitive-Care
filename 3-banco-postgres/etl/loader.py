from etl.extractor import extract_csv

def load_csv_data(conn, file_path, insert_query, batch_size=20000):
    """
    Insere os dados de um arquivo CSV único no banco de dados.

    Args:
        conn: Conexão com o PostgreSQL.
        file_path (str): Caminho do arquivo CSV.
        insert_query (str): Query SQL para inserção dos dados.
        batch_size (int): Tamanho do lote para processamento.
    """
    with conn.cursor() as cur:
        for data in extract_csv(file_path, batch_size=batch_size, sep=';'):
            try:
                cur.executemany(insert_query, data)
                conn.commit()
                print(f"Inserted {cur.rowcount} rows from {file_path}")
            except Exception as err:
                print(f"Erro ao inserir dados do arquivo {file_path}: {err}")
                conn.rollback()

def load_list_data(conn, list_files, queries, batch_size=20000):
    """
    Insere os dados de uma lista de arquivos CSV no banco de dados.
    Seleciona a query de inserção com base no ano presente no nome do arquivo.

    Args:
        conn: Conexão com o PostgreSQL.
        list_files (list): Lista de caminhos para os arquivos CSV.
        queries (dict): Mapeamento entre ano (str) e query de inserção.
        batch_size (int): Tamanho do lote para processamento.
    """
    with conn.cursor() as cur:
        for file_csv in list_files:
            print(f"Processando {file_csv}")
            # Determina qual query utilizar com base no ano encontrado no nome do arquivo
            query = None
            for year, q in queries.items():
                if year in file_csv:
                    query = q
                    break
            if not query:
                print(f"Nenhuma query definida para o arquivo {file_csv}. Pulando.")
                continue
            for data in extract_csv(file_csv, batch_size=batch_size, sep=';'):
                try:
                    cur.executemany(query, data)
                    conn.commit()
                    print(f"Inserted {cur.rowcount} rows from {file_csv}")
                except Exception as err:
                    print(f"Erro ao inserir dados do arquivo {file_csv}: {err}")
                    conn.rollback()
