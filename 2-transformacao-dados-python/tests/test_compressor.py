import os
import pytest
import zipfile
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, mock_open

from src.compressor import compress_and_save, CompressionError

@pytest.fixture
def temp_test_dir():
    """Create a temporary test directory with test files"""
    # Create temp directory
    test_dir = tempfile.mkdtemp()
    output_dir = os.path.join(test_dir, "output")
    os.makedirs(output_dir)
    
    # Create a test CSV file
    test_csv_path = os.path.join(output_dir, "test.csv")
    with open(test_csv_path, 'w') as f:
        f.write("header1,header2\nvalue1,value2\nvalue3,value4")
    
    yield (test_dir, output_dir)
    
    # Clean up after tests
    shutil.rmtree(test_dir)

def test_successful_compression(temp_test_dir):
    """Test that a CSV file is successfully compressed to a ZIP file"""
    _, output_dir = temp_test_dir
    
    compress_and_save("test.csv", "test.zip", output_dir=output_dir)
    
    # Verify the zip file exists
    zip_path = os.path.join(output_dir, "test.zip")
    assert os.path.exists(zip_path)
    
    # Verify the zip file contains the CSV
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        assert "test.csv" in zipf.namelist()

def test_missing_csv_file_error(temp_test_dir):
    """Test that an error is raised when the CSV file doesn't exist"""
    _, output_dir = temp_test_dir
    
    # Run the function with non-existent CSV
    with pytest.raises(CompressionError) as exc_info:
        compress_and_save("nonexistent.csv", "test.zip", output_dir=output_dir)
    
    
    assert "Cannot compress file - source not found" in str(exc_info.value)

def test_permission_error_handling(temp_test_dir):
    """Test that a permission error is properly handled"""
    _, output_dir = temp_test_dir
    
    # Need to add mock for path.exists to return True
    with patch('os.path.exists', return_value=True):
        # Mock zipfile to raise PermissionError
        with patch('zipfile.ZipFile', side_effect=PermissionError("Permission denied")):
            with pytest.raises(CompressionError) as exc_info:
                compress_and_save("test.csv", "test.zip", output_dir=output_dir)
    
    assert "Permission denied" in str(exc_info.value)

def test_bad_zip_error_handling(temp_test_dir):
    """Test that a BadZipFile error is properly handled"""
    _, output_dir = temp_test_dir
    
    # Need to add mock for path.exists to return True
    with patch('os.path.exists', return_value=True):
        # Mock zipfile to raise BadZipFile
        with patch('zipfile.ZipFile', side_effect=zipfile.BadZipFile("Bad zip file")):
            with pytest.raises(CompressionError) as exc_info:
                compress_and_save("test.csv", "test.zip", output_dir=output_dir)
    
    assert "ZIP file creation failed" in str(exc_info.value)

def test_general_exception_handling(temp_test_dir):
    """Test that general exceptions are properly handled"""
    _, output_dir = temp_test_dir
    
    # Mock os.path.exists to return True but then cause an exception in ZipFile
    with patch('os.path.exists', return_value=True):
        with patch('zipfile.ZipFile', side_effect=Exception("Unexpected error")):
            with pytest.raises(CompressionError) as exc_info:
                compress_and_save("test.csv", "test.zip", output_dir=output_dir)
    
    assert "Failed to compress file" in str(exc_info.value)