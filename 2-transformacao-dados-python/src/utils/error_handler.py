import functools
import traceback
import os.path
from .logger import get_logger

logger = get_logger('error_handler')

# Custom exceptions
class ETLError(Exception):
    """Base class for all ETL-related exceptions."""
    pass

class FileError(ETLError):
    """Exception raised for file-related errors."""
    pass

class PDFExtractionError(ETLError):
    """Exception raised for errors during PDF extraction."""
    pass

class DataTransformationError(ETLError):
    """Exception raised for errors during data transformation."""
    pass

class CompressionError(ETLError):
    """Exception raised for errors during file compression."""
    pass

# Decorator for error handling
def handle_errors(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except FileNotFoundError as e:
            error_msg = f"File not found: {e}"
            logger.error(error_msg)
            raise FileError(error_msg) from e
        except PDFExtractionError as e:
            logger.error(f"PDF extraction error: {e}")
            raise
        except DataTransformationError as e:
            logger.error(f"Data transformation error: {e}")
            raise
        except CompressionError as e:
            logger.error(f"Compression error: {e}")
            raise
        except Exception as e:
            error_msg = f"Unexpected error in {func.__name__}: {str(e)}"
            logger.error(f"{error_msg}\n{traceback.format_exc()}")
            raise ETLError(error_msg) from e
    return wrapper

# Helper functions
def validate_file_exists(file_path):
    """Validate that a file exists and raise appropriate error if not."""
    if not os.path.exists(file_path):
        error_msg = f"File not found: {file_path}"
        logger.error(error_msg)
        raise FileError(error_msg)

def validate_data(data, validator_func, error_msg=None):
    """Validate data using the provided validator function."""
    if not validator_func(data):
        msg = error_msg or "Data validation failed"
        logger.error(msg)
        raise DataTransformationError(msg)