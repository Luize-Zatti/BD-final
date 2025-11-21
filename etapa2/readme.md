# Integração PostgreSQL + Redis + CRUD em Python

## 1. Preparação do Ambiente

### 1.1 Ativar o ambiente virtual (venv)

```
venv\Scripts\activate
```

### 1.2 Instalar dependências

```
pip install psycopg2-binary redis python-dotenv
```

---

## 2. Configurar o arquivo `.env`

Adicionar no arquivo `.env` as variaveis do postgresql e do redmi

---

## 3. Iniciar o Redis no Windows

1- Entre na pasta onde o Redis está instalado

2- Inicie o servidor:

```
redis-server.exe redis.windows.conf
```

Deixe esta janela aberta.

---

## 4. Banco PostgreSQL

Certifique-se de ter criado o banco:

```sql
CREATE DATABASE trabalho_bd2;
```

---

## 5. Execução do Programa CRUD

O arquivo principal é:

```
crud_app.py
```

Execute:

```
python crud_app.py
```

O programa irá:

1. Criar tabela no PostgreSQL  
2. Inserir nova pessoa  
3. Ler pessoa  
4. Atualizar  
5. Excluir  
6. Fazer operações de cache no Redis  
