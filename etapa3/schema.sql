-- Tabela PECA
CREATE TABLE peca (
    cod_peca   VARCHAR(10) PRIMARY KEY,
    pnome      VARCHAR(50) NOT NULL,
    cor        VARCHAR(20) NOT NULL,
    peso       NUMERIC(10,2) NOT NULL,
    cidade     VARCHAR(50) NOT NULL,
    preco      NUMERIC(10,2) NOT NULL
);

-- Tabela FORNECEDOR
CREATE TABLE fornecedor (
    cod_fornec  VARCHAR(10) PRIMARY KEY,
    fnome       VARCHAR(50) NOT NULL,
    status      INTEGER     NOT NULL,
    cidade      VARCHAR(50) NOT NULL
);

-- Tabela PROJETO
CREATE TABLE projeto (
    cod_proj  VARCHAR(10) PRIMARY KEY,
    jnome     VARCHAR(80) NOT NULL,
    cidade    VARCHAR(50) NOT NULL
);

-- Tabela FORNECIMENTO (tabela de relacionamento)
CREATE TABLE fornecimento (
    cod_fornec   VARCHAR(10) NOT NULL,
    cod_peca     VARCHAR(10) NOT NULL,
    cod_proj     VARCHAR(10) NOT NULL,
    quantidade   INTEGER     NOT NULL,

    CONSTRAINT pk_fornecimento
        PRIMARY KEY (cod_fornec, cod_peca, cod_proj),

    CONSTRAINT fk_fornecimento_fornecedor
        FOREIGN KEY (cod_fornec) REFERENCES fornecedor(cod_fornec),

    CONSTRAINT fk_fornecimento_peca
        FOREIGN KEY (cod_peca) REFERENCES peca(cod_peca),

    CONSTRAINT fk_fornecimento_projeto
        FOREIGN KEY (cod_proj) REFERENCES projeto(cod_proj)
);
