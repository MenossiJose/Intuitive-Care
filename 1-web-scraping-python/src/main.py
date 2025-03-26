import sys
import os
from pathlib import Path

# Add the project root directory to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.scraping.scraper import get_pdf_links
from src.scraping.downloader import download_files
from src.scraping.compressor import compress_files
from src.config import URL, DOWNLOAD_DIR, ZIP_NAME
from src.utils.logger import get_logger

# Create a logger for the main module
logger = get_logger('main')

def main():
    logger.info("Iniciando processo de web scraping...")
    
    # 1. Extrair os links dos PDFs
    try:
        pdf_links = get_pdf_links(URL)
        if not pdf_links:
            logger.warning("Nenhum link PDF foi encontrado.")
            return
        logger.info(f"Links encontrados: {len(pdf_links)}")
        logger.debug(f"Links detalhados: {pdf_links}")
    except Exception as e:
        logger.error(f"Erro na extração dos links: {e}")
        return
    
    # 2. Realizar o download dos arquivos
    downloaded_files = download_files(pdf_links, DOWNLOAD_DIR)
    if not downloaded_files:
        logger.error("Falha no download dos arquivos.")
        return
    logger.info(f"Arquivos baixados: {len(downloaded_files)}")
    logger.debug(f"Arquivos detalhados: {downloaded_files}")
    
    # 3. Compactar os arquivos baixados
    compress_files(downloaded_files, ZIP_NAME)
    logger.info(f"Arquivos compactados em: {ZIP_NAME}")
    logger.info("Processo finalizado com sucesso!")

if __name__ == '__main__':
    main()