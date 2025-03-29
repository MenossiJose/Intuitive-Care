CREATE TABLE IF NOT EXISTS financial_statements_2023 (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
	reg_ans VARCHAR(50) NOT NULL,
	cd_conta_contabil VARCHAR(50),
	descricao VARCHAR(255),
    vl_saldo_inicial FLOAT,
	vl_saldo_final FLOAT
);

CREATE TABLE IF NOT EXISTS financial_statements_2024 (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    data DATE,
	reg_ans VARCHAR(50) NOT NULL,
	cd_conta_contabil VARCHAR(50),
	descricao VARCHAR(255),
    vl_saldo_inicial FLOAT,
	vl_saldo_final FLOAT
);

CREATE TABLE IF NOT EXISTS active_operators(
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
	registro_ANS VARCHAR(255) NOT NULL,
	cnpj VARCHAR(14),
	razao_social VARCHAR(255),
	nome_fantasia VARCHAR(255),
	modalidade VARCHAR(50),
	logradouro VARCHAR(255),
	numero VARCHAR(50),
	complemento VARCHAR(255),
	bairro VARCHAR(255),
	cidade VARCHAR(255),
	uf VARCHAR(10),
	cep VARCHAR(20),
	ddd	VARCHAR(10),
	telefone VARCHAR(30),
	fax VARCHAR(30),
	endereco_eletronico VARCHAR(255),
	representante VARCHAR(255),
	cargo_representante VARCHAR(255),
    regiao_de_comercializacao VARCHAR(255),
	data_registro_ANS VARCHAR(255)
);

