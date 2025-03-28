import zipfile
import os
from src.utils.error_handler import handle_errors, CompressionError
from src.utils.logger import get_logger
from src.utils.path import get_output_dir

logger = get_logger('compressor')

@handle_errors
def compress_and_save(name_csv, name_zip, output_dir=None):
    try:
        # Path to the output - use the utility if not explicitly specified
        if output_dir is None:
            output_dir = get_output_dir()
            
        # Generate full paths for CSV and ZIP files
        csv_path = os.path.join(output_dir, name_csv)
        zip_path = os.path.join(output_dir, name_zip)
        
        # Validate CSV file exists before attempting to compress
        if not os.path.exists(csv_path):
            raise FileNotFoundError(f"CSV file not found at {csv_path}")
        
        # Create the zip file with the csv file in the output directory
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(name_csv))
        
        logger.info(f"File {zip_path} created successfully!")
        return zip_path
    except FileNotFoundError as e:
        raise CompressionError(f"Cannot compress file - source not found: {str(e)}")
    except PermissionError as e:
        raise CompressionError(f"Permission denied when creating ZIP file: {str(e)}")
    except zipfile.BadZipFile as e:
        raise CompressionError(f"ZIP file creation failed: {str(e)}")
    except Exception as e:
        raise CompressionError(f"Failed to compress file: {str(e)}")