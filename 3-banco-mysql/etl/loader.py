from etl.extractor import extract_csv
from etl.transformer import save_processed_csv

def load_csv_data(session, file_path, model, batch_size=50000, save_processed=True):
    """
    Loads CSV data and inserts records using SQLAlchemy ORM.
    Optionally saves processed data to CSV.
    """
    if save_processed:
        processed_path = save_processed_csv(file_path, batch_size=batch_size, sep=';')
        print(f"Saved processed data to {processed_path}")
    
    # Continue with normal extraction and loading
    for data in extract_csv(file_path, batch_size=batch_size, sep=';'):
        # Skip the id column
        columns = [col for col in model.__table__.columns.keys() if col != 'id']
        
        # Map data to columns, skipping the first field for id
        objects = []
        for row in data:
            if len(row) >= len(columns):
                obj_data = dict(zip(columns, row[:len(columns)]))
                objects.append(model(**obj_data))
        
        try:
            session.bulk_save_objects(objects)
            session.commit()
            print(f"Inserted {len(objects)} rows from {file_path}")
        except Exception as err:
            print(f"Error inserting data from {file_path}: {err}")
            session.rollback()

def load_list_data(session, list_files, model_mapping, batch_size=50000, save_processed=True):
    """
    Loads data from a list of CSV files. 
    """
    for file_csv in list_files:
        model = None
        for year, m in model_mapping.items():
            if year in file_csv:
                model = m
                break
        if not model:
            print(f"No model defined for file {file_csv}. Skipping.")
            continue

        load_csv_data(session, file_csv, model, batch_size, save_processed)