import os
import zipfile
from src.utils.logger import get_logger
from src.utils.error_handler import error_handler, FileOperationError

# Create a logger for this module
logger = get_logger('compressor')

@error_handler
def compress_files(file_list, zip_name):
    """
    Compress a list of files into a zip archive
    
    Args:
        file_list (list): List of file paths to compress
        zip_name (str): Name/path of the output zip file
        
    Returns:
        str: Path to the created zip file
    """
    logger.info(f"Iniciando compressão de {len(file_list)} arquivos para: {zip_name}")
    
    try:
        with zipfile.ZipFile(zip_name, 'w') as zipf:
            for file in file_list:
                if not os.path.exists(file):
                    logger.warning(f"Arquivo não encontrado: {file}")
                    continue
                    
                try:
                    # Add files to the zip file with their basenames
                    basename = os.path.basename(file)
                    zipf.write(file, arcname=basename)
                    logger.debug(f"Arquivo adicionado ao ZIP: {basename}")
                except Exception as e:
                    logger.error(f"Erro ao adicionar {file} ao arquivo ZIP: {e}")
                    raise FileOperationError(f"Failed to add {file} to zip") from e
                    
        logger.info(f"Arquivos compactados com sucesso em: {zip_name}")
        return zip_name
        
    except Exception as e:
        logger.error(f"Erro durante a compressão dos arquivos: {e}")
        raise FileOperationError(f"Failed to create zip file {zip_name}") from e