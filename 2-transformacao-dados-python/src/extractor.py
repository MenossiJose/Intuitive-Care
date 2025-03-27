import pdfplumber
import csv
import os
from zipfile import ZipFile

def extract_table_pdf(pdf_path):
    # Step 1: Extract raw data from PDF
    raw_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                raw_data.extend(table)
    
    if not raw_data:
        return []
    
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