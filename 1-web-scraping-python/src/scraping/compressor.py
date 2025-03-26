import os
import zipfile

def compress_files(file_list, zip_name):
    with zipfile.ZipFile(zip_name, 'w') as zipf:
        for file in file_list:
            # Adiciona o arquivo mantendo apenas o nome
            zipf.write(file, arcname=os.path.basename(file))
    print(f"Arquivos compactados em: {zip_name}")