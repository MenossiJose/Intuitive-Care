import pytest
from unittest.mock import patch, MagicMock
import sys
from pathlib import Path

# Add the parent directory to sys.path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraping.scraper import get_pdf_links


@pytest.fixture
def mock_response():
    """Create a mock successful response"""
    mock_resp = MagicMock()
    mock_resp.status_code = 200
    return mock_resp


def test_get_pdf_links_with_valid_links():
    """Test finding PDF links with 'anexo i' and 'anexo ii'"""
    html_content = """
    <html>
        <body>
            <a href="doc1.pdf">Some document</a>
            <a href="anexo1.pdf">Anexo I - Document</a>
            <a href="anexo2.pdf">ANEXO II Document</a>
            <a href="other.pdf">Other PDF</a>
            <a href="not-pdf.txt">Not a PDF</a>
        </body>
    </html>
    """
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = html_content.encode('utf-8')
        
        result = get_pdf_links("https://example.com")
        
        assert len(result) == 2
        assert "anexo1.pdf" in result
        assert "anexo2.pdf" in result
        assert "doc1.pdf" not in result
        assert "other.pdf" not in result
        assert "not-pdf.txt" not in result


def test_get_pdf_links_with_relative_urls():
    """Test handling of relative URLs in PDF links"""
    html_content = """
    <html>
        <body>
            <a href="/path/anexo1.pdf">Anexo I - Document</a>
            <a href="https://example.com/anexo2.pdf">Anexo II Document</a>
        </body>
    </html>
    """
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = html_content.encode('utf-8')
        
        result = get_pdf_links("https://www.gov.br/page")
        
        assert len(result) == 2
        assert "https://www.gov.br/path/anexo1.pdf" in result
        assert "https://example.com/anexo2.pdf" in result


def test_get_pdf_links_no_matching_links():
    """Test with a page that has no matching PDF links"""
    html_content = """
    <html>
        <body>
            <a href="doc1.pdf">Some document</a>
            <a href="other.pdf">Other PDF</a>
            <a href="not-pdf.txt">Not a PDF</a>
        </body>
    </html>
    """
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = html_content.encode('utf-8')
        
        result = get_pdf_links("https://example.com")
        
        assert len(result) == 0


def test_get_pdf_links_empty_page():
    """Test with an empty page"""
    html_content = "<html><body></body></html>"
    
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = html_content.encode('utf-8')
        
        result = get_pdf_links("https://example.com")
        
        assert len(result) == 0


def test_get_pdf_links_http_error():
    """Test error handling when HTTP request fails"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 404
        
        with pytest.raises(Exception) as excinfo:
            get_pdf_links("https://example.com")
        
        assert "Erro ao acessar o site: 404" in str(excinfo.value)


def test_get_pdf_links_correct_user_agent():
    """Test that the correct User-Agent is sent in the request"""
    with patch('requests.get') as mock_get:
        mock_get.return_value.status_code = 200
        mock_get.return_value.content = b"<html><body></body></html>"
        
        get_pdf_links("https://example.com")
        
        # Check that requests.get was called with the correct headers
        call_kwargs = mock_get.call_args[1]
        assert 'headers' in call_kwargs
        assert 'User-Agent' in call_kwargs['headers']
        # We don't check the exact value since it's imported from config