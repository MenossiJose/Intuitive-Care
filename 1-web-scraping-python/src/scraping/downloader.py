import os
import requests
from src.config import USER_AGENT
from src.utils.logger import get_logger
from src.utils.error_handler import error_handler, handle_request_error, FileOperationError

# Create a logger for this module
logger = get_logger('downloader')

@error_handler
def download_files(links, download_dir):
    """
    Download files from a list of URLs
    
    Args:
        links (list): List of URLs to download
        download_dir (str): Directory to save downloaded files
        
    Returns:
        list: Paths of successfully downloaded files
    """
    logger.info(f"Iniciando download de {len(links)} arquivos para: {download_dir}")
    
    if not os.path.exists(download_dir):
        logger.debug(f"Criando diretório de download: {download_dir}")
        os.makedirs(download_dir)
    
    downloaded_files = []
    headers = {'User-Agent': USER_AGENT}
    
    for link in links:
        file_name = link.split("/")[-1]
        file_path = os.path.join(download_dir, file_name)
        logger.debug(f"Baixando {link} para {file_path}")
        
        try:
            response = requests.get(link, headers=headers)
            
            if response.status_code == 200:
                try:
                    with open(file_path, 'wb') as f:
                        f.write(response.content)
                    downloaded_files.append(file_path)
                    logger.info(f"Arquivo {file_name} baixado com sucesso.")
                except Exception as e:
                    logger.error(f"Erro ao salvar arquivo {file_name}: {e}")
                    raise FileOperationError(f"Failed to write file {file_path}") from e
            else:
                logger.warning(f"Falha no download do arquivo: {file_name} (Status: {response.status_code})")
                handle_request_error(response.raise_for_status(), link)
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Erro durante o download de {link}: {e}")
            handle_request_error(e, link)
    
    logger.info(f"Download concluído. {len(downloaded_files)} arquivos baixados com sucesso.")
    return downloaded_files