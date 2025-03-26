import requests
from bs4 import BeautifulSoup
from config import USER_AGENT

def get_pdf_links(url):
    headers = {'User-Agent': USER_AGENT}
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Erro ao acessar o site: {response.status_code}")
    
    soup = BeautifulSoup(response.content, 'lxml')
    pdf_links = []
    
    # Filtra todos os links que terminam com .pdf
    for a in soup.find_all("a", href=True):
        href = a['href']
        text = a.get_text(strip=True).lower()

        # Verifica se no texto âncora está escrito "anexo i" ou "anexo ii"
        if href.lower().endswith(".pdf") and ("anexo i" in text or "anexo ii" in text):
            # Corrige link relativo se necessário
            if href.startswith("/"):
                href = "https://www.gov.br" + href
            pdf_links.append(href)

    return pdf_links


