# Projeto ETL e Análise de Dados da ANS

Este projeto implementa um pipeline ETL (Extract, Transform, Load) para processar dados de operadoras de saúde da ANS (Agência Nacional de Saúde Suplementar) e realizar análises sobre esses dados.

## Visão Geral

O projeto realiza as seguintes operações:

1. Extrai dados de arquivos CSV de demonstrações financeiras por trimestre (2023-2024)
2. Transforma os dados (conversão de datas, tratamento de valores nulos, etc.)
3. Carrega os dados em um banco de dados MySQL
4. Executa consultas analíticas para identificar as operadoras com maiores despesas

## Componentes Principais

- **ETL Pipeline**: Implementado nos módulos `extractor.py`, `transformer.py` e `loader.py`
- **Modelos de Dados**: Definidos em `models.py`
- **Script Principal**: `main.py` para orquestrar o processo ETL
- **Análises**: `analytics.py` para executar consultas analíticas

## Passo a Passo para Execução

1. **Configuração do Ambiente**

   - Crie e ative um ambiente virtual:

   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```

2. **Configuração do Ambiente**:

   ```
   # Instalar dependências
   pip install -r requirements.txt
   ```

3. **Configurar Variáveis de Ambiente**:

   - Certifique-se de que o arquivo `.env` contém as configurações corretas:

   ```
   DB_HOST=localhost
   DB_PORT=3306
   DB_USER=ansUser
   DB_PASSWORD=ansPassword
   DB_NAME=ansDb
   ```

4. **Preparar o Banco de Dados MySQL**:

   - Garantir que o MySQL está rodando
   - Se quiser usar Docker, execute:

   ```
   cd docker
   docker-compose up -d
   ```

5. **Verificar Arquivos de Dados**:

   - Certifique-se de que os arquivos CSV estão disponíveis em `raw`:
     - Arquivos trimestrais (1-4T2023.csv, 1-4T2024.csv, etc.)
     - Arquivo de operadoras ativas (Relatorio_cadop.csv)

6. **Executar o Pipeline ETL**:

   ```
   python main.py
   ```

   - Este comando cria o schema, extrai, transforma e carrega os dados

7. **Executar Análises**:
   ```
   python analytics.py
   ```
   - Este comando executa as consultas para identificar:
     - Top 10 operadoras com maiores despesas no último trimestre
     - Top 10 operadoras com maiores despesas no último ano

## Arquitetura do Projeto

- Os dados brutos são lidos de `raw`
- Os dados processados são salvos em `processed`
- O processamento ocorre em lotes (chunks) para gerenciar o uso de memória
- As transformações incluem padronização de datas e valores numéricos
- Os dados são armazenados em tabelas relacionais no MySQL

As análises focam em despesas com "EVENTOS/SINISTROS CONHECIDOS OU AVISADOS DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR", um indicador importante do desempenho financeiro das operadoras de saúde.
