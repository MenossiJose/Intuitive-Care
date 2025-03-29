import pandas as pd

def convert_nan_to_none(valor):
    """Converte valores NaN/NaT do pandas para None (NULL no banco de dados)."""
    return None if pd.isna(valor) else valor

def convert_comma_into_period(value):
    """Converte valores com vírgula para pontos."""
    if isinstance(value, str):
        return value.replace(",", ".")
    return value

def convert_date_format(value):
    """Converte datas do formato dd/mm/aaaa para aaaa-mm-dd."""
    if isinstance(value, str):
        if len(value.split('/')) == 3 and len(value) == 10:
            try:
                day, month, year = value.split('/')
                if len(day) == 2 and len(month) == 2 and len(year) == 4:
                    return f"{year}-{month}-{day}"
            except ValueError:
                pass
    return value

def transform_row(row):
    """Aplica as transformações necessárias em cada linha (tupla de valores)."""
    return tuple(
        convert_nan_to_none(
            convert_comma_into_period(
                convert_date_format(value)
            )
        ) for value in row
    )

def extract_csv(file_path, batch_size=20000, sep=';'):
    """
    Gera os dados transformados de um CSV em lotes (chunks).

    Args:
        file_path (str): Caminho do arquivo CSV.
        batch_size (int): Número de linhas por lote.
        sep (str): Delimitador do CSV.

    Yields:
        list: Lista de tuplas contendo os dados transformados.
    """
    for chunk in pd.read_csv(file_path, chunksize=batch_size, sep=sep):
        data = [transform_row(row) for row in chunk.itertuples(index=False, name=None)]
        yield data
