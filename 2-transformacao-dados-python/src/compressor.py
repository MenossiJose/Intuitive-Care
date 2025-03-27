import zipfile
import os

def compress_and_save(name_csv, name_zip):
    try:
        # Path to the output
        output_dir = '../data/output'
        
        # Generate full paths for CSV and ZIP files
        csv_path = os.path.join(output_dir, name_csv)
        zip_path = os.path.join(output_dir, name_zip)
        
        # Create the zip file with the csv file in the output directory
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(csv_path, os.path.basename(name_csv))
        
        print(f"File {zip_path} created successfully!")
    except Exception as e:
        print(f"Error in saving/compressing the file: {e}")
        raise