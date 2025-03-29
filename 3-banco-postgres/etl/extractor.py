import pandas as pd
from etl.transformer import transform_row

def extract_csv(file_path, batch_size=50000, sep=';'):
    """
    Reads a CSV file in chunks and applies transformations to each row.
    """
    for chunk in pd.read_csv(file_path, chunksize=batch_size, sep=sep):
        data = [transform_row(row) for row in chunk.itertuples(index=False, name=None)]
        yield data
