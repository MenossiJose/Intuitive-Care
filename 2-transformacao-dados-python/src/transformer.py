import os
import pandas as pd

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
        print(f"CSV saved to {csv_path}")
        
    except Exception as e:
        print(f"Error in saving the CSV file: {e}")
        raise