import functools
import sys
import traceback
import requests
from pathlib import Path
from src.utils.logger import get_logger

# Setup logger for error handler
logger = get_logger('error_handler')

class WebScrapingError(Exception):
    """Base exception class for web scraping errors"""
    pass

class NetworkError(WebScrapingError):
    """Exception raised for network connectivity issues"""
    pass

class HttpError(WebScrapingError):
    """Exception raised for HTTP error status codes"""
    pass

class ParsingError(WebScrapingError):
    """Exception raised for errors during HTML/content parsing"""
    pass

class FileOperationError(WebScrapingError):
    """Exception raised for errors during file operations"""
    pass

def handle_request_error(error, url):
    """
    Handle request-related errors
    
    Args:
        error: The exception that was raised
        url: The URL that was being accessed
    
    Returns:
        dict: Error information
    """
    error_info = {
        'type': type(error).__name__,
        'message': str(error),
        'url': url,
    }
    
    if isinstance(error, requests.ConnectionError):
        logger.error(f"Connection error accessing {url}: {error}")
        raise NetworkError(f"Failed to connect to {url}") from error
        
    elif isinstance(error, requests.Timeout):
        logger.error(f"Timeout accessing {url}: {error}")
        raise NetworkError(f"Request timed out for {url}") from error
        
    elif isinstance(error, requests.HTTPError):
        logger.error(f"HTTP error accessing {url}: {error}")
        status_code = error.response.status_code if hasattr(error, 'response') else 'unknown'
        raise HttpError(f"HTTP error {status_code} for {url}") from error
        
    else:
        logger.error(f"Unexpected error accessing {url}: {error}")
        return error_info

def handle_file_error(error, file_path, operation):
    """
    Handle file operation errors
    
    Args:
        error: The exception that was raised
        file_path: The path to the file
        operation: The operation being performed (read, write, etc.)
    
    Returns:
        dict: Error information
    """
    error_info = {
        'type': type(error).__name__,
        'message': str(error),
        'file_path': file_path,
        'operation': operation,
    }
    
    logger.error(f"File error during {operation} on {file_path}: {error}")
    raise FileOperationError(f"Failed to {operation} file {file_path}") from error

def error_handler(func):
    """
    Decorator to handle errors in functions
    
    Args:
        func: The function to wrap
    
    Returns:
        function: Wrapped function with error handling
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except WebScrapingError:
            # Already handled and logged, just re-raise
            raise
        except Exception as e:
            # Get function name and args for better error context
            func_name = func.__name__
            args_repr = [repr(a) for a in args]
            kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
            args_str = ", ".join(args_repr + kwargs_repr)
            
            # Log the error with context
            logger.error(f"Error in {func_name}({args_str}): {e}")
            logger.debug(f"Exception traceback: {traceback.format_exc()}")
            
            # Re-raise as a more specific error if possible
            raise
    
    return wrapper

def retry(max_attempts=3, delay=1, backoff=2, exceptions=(Exception,)):
    """
    Retry decorator with exponential backoff
    
    Args:
        max_attempts: Maximum number of attempts
        delay: Initial delay between attempts in seconds
        backoff: Backoff multiplier
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        function: Decorator function
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            import time
            mtries, mdelay = max_attempts, delay
            
            while mtries > 1:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    msg = f"{str(e)}, retrying in {mdelay} seconds..."
                    logger.warning(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
                    
            # Final attempt
            return func(*args, **kwargs)
        return wrapper
    return decorator