from extractor import extract_table_pdf
from compressor import compress_and_save
from transformer import save_to_csv

def main():
    pdf_path = '../data/input/Anexo_I.pdf'  # Certifique-se que o arquivo do Anexo I esteja disponível no diretório
    name_csv = 'dados_extraidos.csv'
    your_name = "JoseMenossi"  # Substitua pelo seu nome
    name_zip = f"Teste_{your_name}.zip"

    # Extração da tabela
    data = extract_table_pdf(pdf_path)

    # Realize testes adicionais para validar a extração (ex: contagem de linhas, verificação de cabeçalhos, etc.)
    # Exemplo: assert not df.empty, "DataFrame vazio após extração!"

    # Substituição das abreviações
    save_to_csv(data, name_csv)

    # Salvando o CSV e compactando
    compress_and_save(name_csv, name_zip)

if __name__ == '__main__':
    main()