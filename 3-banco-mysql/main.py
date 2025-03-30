import time
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.models import Base, FinancialStatement2023, FinancialStatement2024, ActiveOperator
from etl.loader import load_csv_data, load_list_data
from dotenv import load_dotenv
from utils.paths import RAW_DATA_DIR, PROCESSED_DATA_DIR

load_dotenv()

DB_HOST = os.getenv("DB_HOST", "localhost")  
DB_PORT = os.getenv("DB_PORT", 3306) 
DB_USER = os.getenv("DB_USER", "ansUser") 
DB_PASSWORD = os.getenv("DB_PASSWORD", "ansPassword")  
DB_NAME = os.getenv("DB_NAME", "ansDb")

# Create SQLAlchemy engine using pymysql driver
engine = create_engine(f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}", echo=False)
Session = sessionmaker(bind=engine)

# Add this line to debug connection issues
print(f"Connecting to MySQL database: {DB_NAME} at {DB_HOST}:{DB_PORT}")

# Create tables based on the models (if they do not exist yet)
Base.metadata.create_all(engine)
print("Schema created successfully.")

# File paths for data extraction
list_files = [
    str(RAW_DATA_DIR / "4T2024.csv"),
    str(RAW_DATA_DIR / "3T2024.csv"),
    str(RAW_DATA_DIR / "2T2024.csv"),
    str(RAW_DATA_DIR / "1T2024.csv"),
    str(RAW_DATA_DIR / "4T2023.csv"),
    str(RAW_DATA_DIR / "3T2023.csv"),
    str(RAW_DATA_DIR / "2T2023.csv"),
    str(RAW_DATA_DIR / "1T2023.csv"),
]
file_path = str(RAW_DATA_DIR / "Relatorio_cadop.csv")


# Mapping of year to corresponding model class
model_mapping = {
    "2023": FinancialStatement2023,
    "2024": FinancialStatement2024
}


def main():
    initial_time = time.time()
    session = Session()

    # Load active operators data
    load_csv_data(session, file_path, model=ActiveOperator, batch_size=50000)

    # Load financial statements data (based on year from filename)
    load_list_data(session, list_files, model_mapping, batch_size=50000)

    session.close()
    print(f"Execution time: {time.time() - initial_time:.2f} seconds")

if __name__ == "__main__":
    main()
