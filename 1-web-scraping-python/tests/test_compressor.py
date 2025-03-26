import pytest
import os
import tempfile
import zipfile
import sys
from pathlib import Path

# Add the parent directory to sys.path to import the module
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scraping.compressor import compress_files

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files"""
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield tmp_dir

@pytest.fixture
def sample_files(temp_dir):
    """Create sample files for testing compression"""
    file_paths = []
    file_contents = ["content1", "content2", "content3"]
    
    for i, content in enumerate(file_contents, 1):
        file_path = os.path.join(temp_dir, f"test_file{i}.txt")
        with open(file_path, 'w') as f:
            f.write(content)
        file_paths.append(file_path)
    
    return file_paths, file_contents

def test_compress_files_creates_zip(temp_dir, sample_files):
    """Test that compress_files creates a zip file with the specified name"""
    file_paths, _ = sample_files
    zip_path = os.path.join(temp_dir, "test.zip")
    
    compress_files(file_paths, zip_path)
    
    assert os.path.exists(zip_path)
    assert zipfile.is_zipfile(zip_path)

def test_compress_files_includes_all_files(temp_dir, sample_files):
    """Test that all files in the input list are included in the zip"""
    file_paths, _ = sample_files
    zip_path = os.path.join(temp_dir, "test.zip")
    
    compress_files(file_paths, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        assert len(zipf.namelist()) == len(file_paths)
        for file_path in file_paths:
            assert os.path.basename(file_path) in zipf.namelist()

def test_compress_files_uses_basenames(temp_dir, sample_files):
    """Test that only the basenames of the files are used in the zip"""
    file_paths, _ = sample_files
    zip_path = os.path.join(temp_dir, "test.zip")
    
    compress_files(file_paths, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for file_path in file_paths:
            # Verify that full paths are not in the zip
            assert file_path not in zipf.namelist()
            # Verify that only basenames are in the zip
            assert os.path.basename(file_path) in zipf.namelist()

def test_compress_files_with_empty_list(temp_dir):
    """Test compress_files with an empty file list"""
    zip_path = os.path.join(temp_dir, "empty.zip")
    
    compress_files([], zip_path)
    
    assert os.path.exists(zip_path)
    assert zipfile.is_zipfile(zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        assert len(zipf.namelist()) == 0

def test_compress_files_preserves_content(temp_dir, sample_files):
    """Test that the content of the files is preserved in the zip"""
    file_paths, file_contents = sample_files
    zip_path = os.path.join(temp_dir, "test.zip")
    
    compress_files(file_paths, zip_path)
    
    with zipfile.ZipFile(zip_path, 'r') as zipf:
        for file_path, expected_content in zip(file_paths, file_contents):
            basename = os.path.basename(file_path)
            with zipf.open(basename) as f:
                content = f.read().decode('utf-8')
                assert content == expected_content