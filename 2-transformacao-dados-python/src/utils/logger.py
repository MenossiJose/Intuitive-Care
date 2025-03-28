import logging
import os
from datetime import datetime

# Create logs directory if it doesn't exist
logs_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
if not os.path.exists(logs_dir):
    os.makedirs(logs_dir)

# Configure the logger
def setup_logger(name='etl'):
    logger = logging.getLogger(name)
    
    # Only configure handlers if they haven't been added yet
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)
        
        # Create file handler with timestamp in filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = os.path.join(logs_dir, f'etl_{timestamp}.log')
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        
        # Create console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # Create formatter and add to handlers
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # Add handlers to logger
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
    
    return logger

root_logger = setup_logger()

def get_logger(name=None):
    if name:
        return logging.getLogger(f'etl.{name}')
    return root_logger