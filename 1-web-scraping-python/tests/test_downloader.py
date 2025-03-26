import pytest
import os
import tempfile
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock


# Add the parent directory to sys.path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraping.downloader import download_files

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir

@pytest.fixture
def mock_response():
    """Create a mock response object"""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = b"test content"
    return mock_resp

@pytest.fixture
def mock_failed_response():
    """Create a mock failed response object"""
    mock_resp = MagicMock()
    mock_resp.status_code = 404
    return mock_resp

def test_download_files_creates_directory(temp_dir):
    """Test that download_files creates the download directory if it doesn't exist"""
    download_dir = os.path.join(temp_dir, "downloads")
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        download_files([], download_dir)
        
    assert os.path.exists(download_dir)

def test_download_files_with_successful_download(temp_dir, mock_response):
    """Test successful file downloads"""
    download_dir = os.path.join(temp_dir, "downloads")
    test_links = ["http://example.com/file1.pdf", "http://example.com/file2.pdf"]
    
    with patch('requests.get', return_value=mock_response) as mock_get:
        result = download_files(test_links, download_dir)
        
        assert len(result) == 2
        assert os.path.join(download_dir, "file1.pdf") in result
        assert os.path.join(download_dir, "file2.pdf") in result
        assert os.path.exists(os.path.join(download_dir, "file1.pdf"))
        assert os.path.exists(os.path.join(download_dir, "file2.pdf"))
        assert mock_get.call_count == 2

def test_download_files_with_failed_download(temp_dir, mock_failed_response):
    """Test handling of failed downloads"""
    download_dir = os.path.join(temp_dir, "downloads")
    test_links = ["http://example.com/file1.pdf", "http://example.com/file2.pdf"]
    
    with patch('requests.get', return_value=mock_failed_response) as mock_get:
        result = download_files(test_links, download_dir)
        
        assert len(result) == 0
        assert not os.path.exists(os.path.join(download_dir, "file1.pdf"))
        assert not os.path.exists(os.path.join(download_dir, "file2.pdf"))
        assert mock_get.call_count == 2

def test_download_files_with_mixed_results(temp_dir, mock_response, mock_failed_response):
    """Test handling of mixed successful and failed downloads"""
    download_dir = os.path.join(temp_dir, "downloads")
    test_links = ["http://example.com/file1.pdf", "http://example.com/file2.pdf"]
    
    with patch('requests.get', side_effect=[mock_response, mock_failed_response]) as mock_get:
        result = download_files(test_links, download_dir)
        
        assert len(result) == 1
        assert os.path.join(download_dir, "file1.pdf") in result
        assert os.path.exists(os.path.join(download_dir, "file1.pdf"))
        assert not os.path.exists(os.path.join(download_dir, "file2.pdf"))
        assert mock_get.call_count == 2

def test_download_files_with_empty_list(temp_dir):
    """Test download_files with an empty links list"""
    download_dir = os.path.join(temp_dir, "downloads")
    
    with patch('requests.get') as mock_get:
        result = download_files([], download_dir)
        
        assert len(result) == 0
        assert not mock_get.called

def test_download_files_saves_correct_content(temp_dir):
    """Test that the downloaded content is correctly saved to file"""
    download_dir = os.path.join(temp_dir, "downloads")
    test_links = ["http://example.com/file1.pdf"]
    test_content = b"This is test content for the file"
    
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    mock_resp.content = test_content
    
    with patch('requests.get', return_value=mock_resp):
        result = download_files(test_links, download_dir)
        
        file_path = os.path.join(download_dir, "file1.pdf")
        assert os.path.exists(file_path)
        with open(file_path, 'rb') as f:
            saved_content = f.read()
        assert saved_content == test_content

def test_download_files_uses_correct_user_agent(temp_dir, mock_response):
    """Test that the User-Agent header is properly set"""
    download_dir = os.path.join(temp_dir, "downloads")
    test_links = ["http://example.com/file1.pdf"]
    
    with patch('requests.get', return_value=mock_response) as mock_get:
        with patch('src.scraping.downloader.USER_AGENT', 'TestUserAgent'):
            download_files(test_links, download_dir)
            
            mock_get.assert_called_once_with(
                test_links[0], 
                headers={'User-Agent': 'TestUserAgent'}
            )