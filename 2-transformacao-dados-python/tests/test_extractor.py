import pytest
from unittest.mock import patch, MagicMock
from src.extractor import extract_table_pdf, PDFExtractionError
import pdfplumber

class MockPage:
    def __init__(self, table_data=None):
        self.table_data = table_data
    
    def extract_table(self):
        return self.table_data

class MockPDF:
    def __init__(self, pages_data):
        self.pages = [MockPage(data) for data in pages_data]
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

@pytest.fixture
def mock_pdf_with_tables():
    """Mock PDF with tables containing abbreviations"""
    # Create mock data - header row + 2 data rows with abbreviations
    pages_data = [
        [
            ["ID", "Name", "Type"],
            [1, "Company A", "OD"],
            [2, "Company B", "AMB"]
        ]
    ]
    return MockPDF(pages_data)

@pytest.fixture
def mock_pdf_no_tables():
    """Mock PDF without any tables"""
    pages_data = [None]
    return MockPDF(pages_data)

@pytest.fixture
def mock_pdf_multiple_pages():
    """Mock PDF with tables across multiple pages"""
    pages_data = [
        [
            ["ID", "Name", "Type"],
            [1, "Company A", "OD"]
        ],
        [
            [3, "Company C", "AMB"],
            [4, "Company D", "OD"]
        ]
    ]
    return MockPDF(pages_data)

# Tests
def test_successful_extraction(mock_pdf_with_tables):
    """Test successful data extraction with abbreviation replacement"""
    with patch('pdfplumber.open', return_value=mock_pdf_with_tables):
        result = extract_table_pdf("fake.pdf")
        
        # Check that we got the expected data rows
        assert len(result) == 2
        assert result[0][2] == "Seg. Odontológica"  # OD replacement
        assert result[1][2] == "Seg. Ambulatorial"  # AMB replacement

def test_empty_pdf(mock_pdf_no_tables):
    """Test handling of PDFs without tables"""
    with patch('pdfplumber.open', return_value=mock_pdf_no_tables):
        result = extract_table_pdf("empty.pdf")
        assert result == []

def test_multiple_pages(mock_pdf_multiple_pages):
    """Test extraction from multiple pages"""
    with patch('pdfplumber.open', return_value=mock_pdf_multiple_pages):
        result = extract_table_pdf("multipage.pdf")
        
        # Should get 3 data rows (skipping header)
        assert len(result) == 3
        # Check replacements
        assert result[0][2] == "Seg. Odontológica"
        assert result[1][2] == "Seg. Ambulatorial"
        assert result[2][2] == "Seg. Odontológica"

def test_non_matching_abbreviations(mock_pdf_with_tables):
    """Test handling of cells without matching abbreviations"""
    # Modify the abbreviation in the mock data
    mock_pdf_with_tables.pages[0].table_data[1][2] = "UNKNOWN"
    
    with patch('pdfplumber.open', return_value=mock_pdf_with_tables):
        result = extract_table_pdf("fake.pdf")
        
        # Check that non-matching abbreviation is left unchanged
        assert result[0][2] == "UNKNOWN"
        # Check that matching abbreviation is still replaced
        assert result[1][2] == "Seg. Ambulatorial"