import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.extractor import extract_table_pdf
from src.compressor import compress_and_save
from src.transformer import save_to_csv
from src.utils.logger import get_logger
from src.utils.error_handler import handle_errors, validate_file_exists
from src.utils.path import get_input_dir, get_output_dir

logger = get_logger('main')

@handle_errors
def main():
    input_dir = get_input_dir()
    output_dir = get_output_dir()

    pdf_path = os.path.join(input_dir, "Anexo_I.pdf")
    name_csv = 'dados_extraidos.csv'
    your_name = "JoseMenossi"
    name_zip = f"Teste_{your_name}.zip"

    # Validate that the PDF file exists
    validate_file_exists(pdf_path)
    
    logger.info(f"Starting data extraction from {pdf_path}")
    data = extract_table_pdf(pdf_path)
    
    # Validate extracted data
    if not data:
        logger.warning("No data was extracted from the PDF")
    else:
        logger.info(f"Successfully extracted {len(data)} rows from PDF")

    # Save to CSV
    logger.info(f"Saving data to CSV: {name_csv}")
    save_to_csv(data, name_csv)
    
    # Compress the CSV file
    logger.info(f"Compressing file to {name_zip}")
    compress_and_save(name_csv, name_zip)
    
    logger.info("Process completed successfully")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logger.error(f"ETL process failed: {str(e)}")
        exit(1)