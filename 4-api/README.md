# Intuitive Care - API

Este projeto é uma aplicação full-stack que permite consultar e analisar dados de operadoras de saúde no Brasil. A aplicação consiste em um backend em FastAPI e um frontend em Vue.js.

## Estrutura do Projeto

```
📁 4-api/
├── 📁 backend/         # API em FastAPI
└── 📁 frontend/        # Interface em Vue.js
```

## Backend (FastAPI)

O backend é uma API REST que fornece endpoints para buscar informações sobre operadoras de saúde.

### Tecnologias Utilizadas

- **FastAPI**: Framework web moderno para construção de APIs
- **SQLAlchemy**: ORM para interação com o banco de dados
- **PyMySQL**: Cliente MySQL para Python
- **Python-dotenv**: Carregamento de variáveis de ambiente
- **Pytest**: Framework de testes

### Estrutura do Backend

```
📁 backend/
├── 📄 requirements.txt    # Dependências do projeto
├── 📄 .env                # Variáveis de ambiente (não commitado)
└── 📁 app/
    ├── 📄 main.py         # Ponto de entrada da aplicação
    ├── 📁 api/            # Definição dos endpoints
    ├── 📁 core/           # Configurações básicas
    ├── 📁 models/         # Modelos de dados
    ├── 📁 schemas/        # Schemas de validação
    ├── 📁 services/       # Lógica de negócios
    ├── 📁 utils/          # Funções utilitárias
    └── 📁 tests/          # Testes unitários
```

### Endpoints da API

- `/api/buscar_nome` - Busca operadoras por nome fantasia
- `/api/buscar_detalhada_nome` - Busca detalhada de operadoras por nome
- `/api/buscar_cnpj` - Busca operadoras por CNPJ
- `/api/buscar_detalhada_cnpj` - Busca detalhada de operadoras por CNPJ
- `/api/buscar_razao_social` - Busca operadoras por razão social
- `/api/buscar_cidade_uf` - Busca operadoras por cidade
- `/api/buscar_modalidade` - Busca operadoras por modalidade

## Frontend (Vue.js)

O frontend é uma aplicação web que permite ao usuário interagir com a API e visualizar os resultados.

### Tecnologias Utilizadas

- **Vue.js 3**: Framework JavaScript progressivo
- **Vue Router**: Roteamento para navegação
- **Axios**: Cliente HTTP para fazer requisições à API
- **Vite**: Ferramenta de build e desenvolvimento

### Estrutura do Frontend

```
📁 frontend/
├── 📄 index.html        # Página HTML principal
├── 📄 package.json      # Dependências e scripts
├── 📄 vite.config.js    # Configuração do Vite
└── 📁 src/
    ├── 📄 App.vue       # Componente raiz
    ├── 📄 main.js       # Ponto de entrada JavaScript
    ├── 📁 assets/       # Recursos estáticos
    ├── 📁 components/   # Componentes reutilizáveis
    ├── 📁 pages/        # Componentes de página
    ├── 📁 router/       # Configuração de rotas
    └── 📁 services/     # Serviços para chamadas à API
```

### Páginas

- **Home**: Página inicial com uma breve descrição do sistema
- **Resultados**: Página que permite realizar pesquisas e exibir resultados

### Funcionalidades

- Pesquisa de operadoras por diferentes critérios:
  - Nome fantasia
  - CNPJ
  - Razão social
  - Modalidade
  - Cidade
- Exibição de resultados em formato tabular
- Interface responsiva

## Como Executar o Projeto

### Backend

1. Navegue até a pasta do backend:
   ```
   cd backend
   ```
2. Crie e ative um ambiente virtual:
   ```
   python -m venv venv
   venv\Scripts\activate  # Windows
   source venv/bin/activate  # Linux/Mac
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Configure o arquivo .env com a URL de conexão ao banco de dados:
   ```
   DATABASE_URL=mysql+pymysql://usuario:senha@localhost/nome_do_banco
   ```
5. Certifique-se que o BD criado em Docker no item anterior está rodando
   ```
   cd Intuitive-Cara/3-banco-mysql/docker
   docker compose up
   ```
6. Execute a API:
   ```
   uvicorn app.main:app --reload
   ```

### Frontend

1. Navegue até a pasta do frontend:
   ```
   cd frontend
   ```
2. Instale as dependências:
   ```
   npm install
   ```
3. Execute o servidor de desenvolvimento:
   ```
   npm run dev
   ```
4. Acesse a aplicação em http://localhost:5173

### Testes

Para executar os testes do backend:

```
cd backend
pytest tests/test_operadora.py
```

### Postman

Postman foi utilizado para testar a api.

![Screenshot](postman.png)
