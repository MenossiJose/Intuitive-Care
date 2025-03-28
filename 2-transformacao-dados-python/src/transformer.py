import os
import pandas as pd
from src.utils.error_handler import handle_errors, DataTransformationError
from src.utils.logger import get_logger

logger = get_logger('transformer')

@handle_errors
def save_to_csv(data, name_csv):
    try:
        # Create output directory if it doesn't exist
        output_dir = '../data/output'
        os.makedirs(output_dir, exist_ok=True)

        # Generate full paths for CSV file
        csv_path = os.path.join(output_dir, name_csv)

        # Create a DataFrame from the data
        df = pd.DataFrame(data)
        
        # Save the dataframe to the output directory
        df.to_csv(csv_path, index=False, encoding='utf-8')
        logger.info(f"CSV saved to {csv_path}")
        
    except pd.errors.EmptyDataError as e:
        raise DataTransformationError(f"Cannot create CSV from empty data: {str(e)}")
    except PermissionError as e:
        raise DataTransformationError(f"Permission denied when writing CSV file: {str(e)}")
    except Exception as e:
        raise DataTransformationError(f"Failed to save data to CSV: {str(e)}")