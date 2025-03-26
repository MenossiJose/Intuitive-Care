# Web Scraping

## Features

- **Web Scraping**: Extracts links to PDF documents from specified URLs
- **Automatic Download**: Downloads all identified PDF files
- **Compression**: Compresses downloaded files into a ZIP archive
- **Robust Error Handling**: Includes comprehensive error handling for network issues, HTTP errors, and file operations
- **Detailed Logging**: Logs all operations to both console and log files for monitoring and debugging

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/Intuitive-Care/1-web-scraping-python.git
   cd web-scraping-python

   ```

2. Clone the repository:

   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate

   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the main script to start the scraping process:

```bash
python src/main.py

```

This will:

1. Extract PDF links from the configured URL
2. Download the PDF files to the downloads directory
3. Compress the files into anexos.zip

## Configuration

The project's behavior can be configured in config.py:

- **URL**: The website URL to scrape
- **DOWNLOAD_DIR**: Directory where downloaded files will be saved
- **ZIP_NAME**: Name of the compressed ZIP file
- **USER_AGENT**: Browser user-agent to use for requests

## Testing

Run the test suite with:

```bash
pytest tests/
```

Or test specific components:

```bash
pytest tests/test_scraper.py
pytest tests/test_downloader.py
pytest tests/test_compressor.py
```
