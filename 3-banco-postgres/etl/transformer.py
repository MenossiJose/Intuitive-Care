import pandas as pd
import os
from pathlib import Path

def convert_nan_to_none(value):
    """Converts NaN/NaT values from pandas to None (NULL in the database)."""
    return None if pd.isna(value) else value

def convert_comma_into_period(value):
    """Converts comma to period in string values."""
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


def save_processed_csv(input_path, output_dir=None, batch_size=50000, sep=';'):
    input_path = Path(input_path)
    
    # Determine output directory
    if output_dir is None:
        output_dir = input_path.parent.parent / "processed"
    else:
        output_dir = Path(output_dir)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define output path
    output_path = output_dir / f"processed_{input_path.name}"
    
    # Process in chunks
    first_chunk = True
    for chunk in pd.read_csv(input_path, chunksize=batch_size, sep=sep):
        # Transform data
        processed_data = [transform_row(row) for row in chunk.itertuples(index=False, name=None)]
        processed_df = pd.DataFrame(processed_data, columns=chunk.columns)
        
        # Write to CSV (first chunk with header, others append)
        mode = 'w' if first_chunk else 'a'
        header = first_chunk
        processed_df.to_csv(output_path, index=False, sep=sep, mode=mode, header=header)
        first_chunk = False
    
    return str(output_path)