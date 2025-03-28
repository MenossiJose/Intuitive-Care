import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent

def get_input_dir():
    """Get the absolute path to the input directory"""
    input_dir = os.path.join(PROJECT_ROOT, 'data', 'input')
    os.makedirs(input_dir, exist_ok=True)
    return input_dir

def get_output_dir():
    """Get the absolute path to the output directory"""
    output_dir = os.path.join(PROJECT_ROOT, 'data', 'output')
    os.makedirs(output_dir, exist_ok=True)
    return output_dir