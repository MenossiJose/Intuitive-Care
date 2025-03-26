from scraping.scraper import get_pdf_links
from scraping.downloader import download_files
from scraping.compressor import compress_files
from config import URL, DOWNLOAD_DIR, ZIP_NAME

def main():
    print("Iniciando processo de web scraping...")
    
    # 1. Extrair os links dos PDFs
    try:
        pdf_links = get_pdf_links(URL)
        if not pdf_links:
            print("Nenhum link PDF foi encontrado.")
            return
        print(f"Links encontrados: {pdf_links}")
    except Exception as e:
        print(f"Erro na extração dos links: {e}")
        return
    
    # 2. Realizar o download dos arquivos
    downloaded_files = download_files(pdf_links, DOWNLOAD_DIR)
    if not downloaded_files:
        print("Falha no download dos arquivos.")
        return
    print(f"Arquivos baixados: {downloaded_files}")
    
    # 3. Compactar os arquivos baixados
    compress_files(downloaded_files, ZIP_NAME)
    print("Processo finalizado com sucesso!")

if __name__ == '__main__':
    main()