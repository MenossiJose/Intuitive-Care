import pdfplumber
from src.utils.error_handler import handle_errors, PDFExtractionError
from src.utils.logger import get_logger

logger = get_logger('extractor')

@handle_errors
def extract_table_pdf(pdf_path):
    logger.info(f"Extracting tables from {pdf_path}")
    try:
        # Step 1: Extract raw data from PDF
        raw_data = []
        with pdfplumber.open(pdf_path) as pdf:
            for i, page in enumerate(pdf.pages):
                logger.debug(f"Processing page {i+1}")
                table = page.extract_table()
                if table:
                    raw_data.extend(table)
        
        if not raw_data:
            logger.warning("No tables found in the PDF")
            return []
        
        logger.info(f"Extracted {len(raw_data)} rows of raw data")
        
        # Skip the header row (first row)
        data_rows = raw_data[1:]
        
        # Process rows and replace abbreviations
        for row in data_rows:
            for i, cell in enumerate(row):
                if cell == 'OD':
                    row[i] = 'Seg. Odontológica'
                elif cell == 'AMB':
                    row[i] = 'Seg. Ambulatorial'
        
        return data_rows
        
    except pdfplumber.PDFSyntaxError as e:
        raise PDFExtractionError(f"Invalid or corrupted PDF: {str(e)}")
    except Exception as e:
        raise PDFExtractionError(f"Failed to extract data from PDF: {str(e)}")