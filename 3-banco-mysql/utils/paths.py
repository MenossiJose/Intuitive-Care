from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Directory for raw data
RAW_DATA_DIR = BASE_DIR / "data" / "raw"

# Directory for processed data
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"

# Example of other paths you might have
SCHEMA_FILE = BASE_DIR / "sql" / "schemas.sql"

# Directory for ETL scripts
ORM_MODELS_DIR = BASE_DIR / "models" / "models.py"

