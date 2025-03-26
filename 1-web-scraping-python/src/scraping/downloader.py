import os
import requests
from config import USER_AGENT

def download_files(links, download_dir):
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    
    downloaded_files = []
    headers = {'User-Agent': USER_AGENT}
    
    for link in links:
        file_name = link.split("/")[-1]
        file_path = os.path.join(download_dir, file_name)
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            downloaded_files.append(file_path)
            print(f"Arquivo {file_name} baixado com sucesso.")
        else:
            print(f"Falha no download do arquivo: {file_name}")
    
    return downloaded_files