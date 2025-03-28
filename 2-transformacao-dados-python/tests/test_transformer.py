import os
import pytest
import pandas as pd
import tempfile
import shutil
from unittest.mock import patch, MagicMock
from src.transformer import save_to_csv, DataTransformationError

@pytest.fixture
def sample_data():
    """Sample data for testing"""
    return [
        ["Row1Col1", "Row1Col2"],
        ["Row2Col1", "Row2Col2"]
    ]

@pytest.fixture
def temp_test_dir():
    """Create a temporary test directory"""
    test_dir = tempfile.mkdtemp()
    output_dir = os.path.join(test_dir, "output")
    os.makedirs(output_dir)
    
    yield (test_dir, output_dir)
    
    # Clean up after tests
    shutil.rmtree(test_dir)

def test_successful_csv_creation(sample_data, temp_test_dir, monkeypatch):
    """Test successful CSV file creation"""
    _, output_dir = temp_test_dir
    
    # Mock the logger to avoid actual logging
    mock_logger = MagicMock()
    monkeypatch.setattr('src.transformer.logger', mock_logger)
    
    original_join = os.path.join
    
    def mock_join(*args):
        if args and args[-1] == "test_output.csv":
            return original_join(output_dir, "test_output.csv")
        return original_join(*args)
    
    with patch('os.path.join', side_effect=mock_join):
        save_to_csv(sample_data, "test_output.csv")
    
    # Check the file was created
    csv_path = os.path.join(output_dir, "test_output.csv")
    assert os.path.exists(csv_path)
    
    # Check file content
    df = pd.read_csv(csv_path)
    assert df.shape == (2, 2)  # 2 rows, 2 columns
    assert df.iloc[0, 0] == "Row1Col1"
    assert df.iloc[1, 1] == "Row2Col2"

def test_empty_data_handling():
    """Test handling of empty data"""
    with patch('os.makedirs'):
        with patch('pandas.DataFrame') as mock_df:
            mock_df.side_effect = pd.errors.EmptyDataError("Empty data")
            
            with pytest.raises(DataTransformationError) as exc_info:
                save_to_csv([], "empty.csv")
            
            assert "Cannot create CSV from empty data" in str(exc_info.value)

def test_permission_error_handling(sample_data):
    """Test handling of permission errors"""
    with patch('os.makedirs'):
        with patch('pandas.DataFrame') as mock_df:
            mock_instance = MagicMock()
            mock_df.return_value = mock_instance
            mock_instance.to_csv.side_effect = PermissionError("Permission denied")
            
            with pytest.raises(DataTransformationError) as exc_info:
                save_to_csv(sample_data, "permission_denied.csv")
            
            assert "Permission denied when writing CSV file" in str(exc_info.value)

def test_general_exception_handling(sample_data):
    """Test handling of general exceptions"""
    with patch('os.makedirs'):
        with patch('pandas.DataFrame') as mock_df:
            mock_instance = MagicMock()
            mock_df.return_value = mock_instance
            mock_instance.to_csv.side_effect = Exception("Unexpected error")
            
            with pytest.raises(DataTransformationError) as exc_info:
                save_to_csv(sample_data, "error.csv")
            
            assert "Failed to save data to CSV" in str(exc_info.value)

def test_directory_creation():
    """Test that output directory is created if it doesn't exist"""
    with patch('os.makedirs') as mock_makedirs:
        with patch('pandas.DataFrame'):
            with patch('os.path.join', return_value="mocked/path.csv"):
                with patch.object(pd.DataFrame, 'to_csv'):
                    save_to_csv([["data"]], "test.csv")
                    
                    # Check that makedirs was called with exist_ok=True
                    mock_makedirs.assert_called_once()
                    args, kwargs = mock_makedirs.call_args
                    assert kwargs.get('exist_ok', False) is True