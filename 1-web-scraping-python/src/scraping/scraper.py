import requests
from bs4 import BeautifulSoup
from src.config import USER_AGENT
from src.utils.logger import get_logger
from src.utils.error_handler import error_handler, handle_request_error, ParsingError, HttpError

# Create a logger for this module
logger = get_logger('scraper')

@error_handler
def get_pdf_links(url):
    """
    Extract PDF links from a webpage that match criteria
    
    Args:
        url (str): URL of the webpage to scrape
        
    Returns:
        list: List of matching PDF URLs
    """
    logger.info(f"Iniciando busca por PDFs em: {url}")
    
    headers = {'User-Agent': USER_AGENT}
    logger.debug(f"Fazendo requisição com User-Agent: {USER_AGENT}")
    
    try:
        response = requests.get(url, headers=headers)
        logger.debug(f"Status code da resposta: {response.status_code}")

        if response.status_code != 200:
            error_msg = f"Erro ao acessar o site: {response.status_code}"
            logger.error(error_msg)
            raise HttpError(error_msg)
        
        logger.info("Resposta recebida com sucesso, analisando conteúdo HTML")
        
        try:
            soup = BeautifulSoup(response.content, 'lxml')
            pdf_links = []
            
            # Filter every link that ends with .pdf
            logger.debug("Procurando links de PDF com referências a 'anexo i' ou 'anexo ii'")
            for a in soup.find_all("a", href=True):
                href = a['href']
                text = a.get_text(strip=True).lower()

                # Verifies if the link is a PDF and contains the text "anexo i" or "anexo ii"
                if href.lower().endswith(".pdf") and ("anexo i" in text or "anexo ii" in text):
                    # Correct the href if it starts with "/"
                    if href.startswith("/"):
                        href = "https://www.gov.br" + href
                        logger.debug(f"URL relativa corrigida: {href}")
                    
                    logger.debug(f"PDF encontrado: {href}")
                    pdf_links.append(href)

            logger.info(f"Busca concluída. {len(pdf_links)} PDFs encontrados.")
            return pdf_links
            
        except Exception as e:
            logger.error(f"Erro ao analisar o HTML: {e}")
            raise ParsingError(f"Failed to parse HTML from {url}") from e
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro ao acessar {url}: {e}")
        handle_request_error(e, url)