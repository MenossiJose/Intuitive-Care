#Transformação de dados em python

Este projeto consiste em um sistema ETL (Extract, Transform, Load) que processa dados de um documento PDF da ANS (Agência Nacional de Saúde Suplementar), extraindo tabelas, transformando-as em formato estruturado e disponibilizando em formato compactado.

## Estrutura do Projeto

```
├──📁 src/                # Código fonte principal
│   ├──📄 __init__.py     # Define os módulos disponíveis
│   ├──📄 extractor.py    # Extração de tabelas do PDF
│   ├──📄 transformer.py  # Transformação de dados para CSV
│   ├──📄 compressor.py   # Compressão de arquivos em ZIP
│   └── utils/          # Utilitários (erros, logs, caminhos)
├──📁 data/               # Diretórios de dados
│   ├──📁 input/          # Arquivos de entrada (Anexo_I.pdf)
│   └──📁 output/         # Arquivos gerados (CSV, ZIP)
├──📁 logs/               # Logs de execução
├──📁 tests/              # Testes unitários
├──📄 requirements.txt    # Dependências do projeto
└──📄 .gitignore          # Arquivos ignorados pelo git
```

## Passo a Passo do Funcionamento

1. **Extração (Extractor)**:

   - Lê o arquivo "Anexo_I.pdf" do diretório de entrada
   - Utiliza a biblioteca `pdfplumber` para extrair tabelas do PDF
   - Processa as informações de procedimentos médicos e coberturas

2. **Transformação (Transformer)**:

   - Converte os dados extraídos em um formato estruturado
   - Normaliza os dados (ex: converte "AMB" para "Seg. Ambulatorial" e "OD" para "Seg. Odontológica")
   - Salva os dados em formato CSV com o nome "dados_extraidos.csv"

3. **Carga (compressor)**:
   - Compacta o arquivo CSV em um arquivo ZIP
   - Nomeia o arquivo como "Teste_JoseMenossi.zip"
   - Salva no diretório de saída

## Ferramentas Principais

1. **pdfplumber**: Biblioteca para extração de conteúdo de PDFs
2. **pandas**: Manipulação e análise de dados estruturados
3. **tabula-py**: Extração de tabelas específicas de PDFs
4. **zipfile**: (embutido no Python) Para compressão de arquivos

## Configuração do Ambiente

### 1. Criação do Ambiente Virtual

```
# Usando venv (recomendado)
python -m venv venv

# Ativação no Windows
venv\Scripts\activate

# Ativação no macOS/Linux
source venv/bin/activate
```

### 2. Instalação das Dependências

```
# Instalar todas as dependências listadas no requirements.txt
pip install -r requirements.txt
```

### 3. Executar Processo

```
python src/main.py
```

## Uso do Projeto

1. Coloque o arquivo "Anexo_I.pdf" na pasta input
2. Execute o script principal:
   ```
   python src/main.py
   ```
3. Verifique os resultados em output e os logs em logs

## Dependências Principais

- **pandas (2.2.3)**: Manipulação de dados tabulares
- **pdfplumber (0.11.5)**: Extração de conteúdo de PDFs
- **pypdf/PyPDF2**: Manipulação geral de arquivos PDF

### Testes

Para executar os testes:

```
pytest tests/
```
