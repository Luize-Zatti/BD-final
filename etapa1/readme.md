# Documentação de Preparação do Ambiente (Python + Neo4j)

Este documento registra **todos os passos executados**, conforme solicitado na atividade da disciplina.  
A linguagem utilizada no exemplo é **Python**.

---
## 1. Instalar o Python
Verifique se o Python já está instalado:

```bash
python --version
```

Caso não esteja instalado, baixe em: https://www.python.org/downloads/

---

## 2. Criar um diretório para o projeto

Escolha um local no computador e crie a pasta:

```bash
mkdir trabalhoF_bd
cd trabalhoF_bd
```

---

## 3. Criar uma venv (ambiente virtual)

```bash
python -m venv venv
```
---

## 4. Ativar o ambiente virtual

### Windows (PowerShell):
```bash
venv\Scripts\activate
```

Quando ativado, o terminal deve mostrar algo como:
```
(venv) C:\Users\...\>
```

---

## 5. Instalar a biblioteca do Neo4j

```bash
pip install neo4j
```

Para confirmar:

```bash
pip list
```

---

## 6. Iniciar a instância do Neo4j

1. Abra o **Neo4j Desktop** ou **Neo4j online**.
2. Clique em **Start** para iniciar o banco.
3. Anote:
   - URI (geralmente: `bolt://localhost:7687`)
   - Usuário
   - Senha

---

## 7. Escolher uma IDE
Para o desenvolvimento do projeto utilizaremos o Visual Studio Code (VSCode).

---

## 8. Instalar a extensão Python no VSCode

No VSCode:
1. Pressione **CTRL+SHIFT+X**
2. Pesquise por: `Python`
3. Clique em **Install**

---

## 9. Abrir a pasta do projeto no VSCode

No menu:
**File → Open Folder → selecione a pasta `trabalhoF_bd/`**

---

## 10. (Opcional) Testar a conexão com o Neo4j

Crie um arquivo `test_connection.py`:

```python
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "SUA_SENHA"

driver = GraphDatabase.driver(uri, auth=(user, password))

def test_db(tx):
    return tx.run("RETURN 'Conexão bem-sucedida!' AS msg").single()["msg"]

with driver.session() as session:
    print(session.execute_write(test_db))
```

Execute:

```bash
python test_connection.py
```

---

### 12. Teste do código `consulta_pessoas.py`

Após criar o arquivo `consulta_pessoas.py` com o código de exemplo do slide, executei o comando:

```bash
python consulta_pessoas.py
```
---


## 13) Métodos da classe `Driver` na biblioteca Neo4j para Python

> *Conforme orientação da atividade, esta seção foi elaborada com auxílio de uma ferramenta de IA (ChatGPT, da OpenAI), e o conteúdo foi revisado antes de ser incluído.*

Na biblioteca oficial do Neo4j para Python, a conexão com o banco é representada pela classe `Driver`, criada normalmente com:

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri, auth=(user, password))
```

Alguns métodos dessa classe são particularmente importantes no uso comum da biblioteca.

### 13.1 `driver.session()`

Cria uma **sessão de trabalho** com o banco de dados.  
É dentro da sessão que as instruções Cypher são executadas.

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri, auth=(user, password))

with driver.session(database="neo4j") as session:
    result = session.run("MATCH (p:Pessoa) RETURN p.nome AS nome")
    for record in result:
        print(record["nome"])

driver.close()
```

### 13.2 `driver.verify_connectivity()`

Verifica se o driver consegue se conectar ao banco de dados com sucesso.  
É útil principalmente na fase de configuração do ambiente.

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri, auth=(user, password))

# Verifica se a conexão está funcional
driver.verify_connectivity()
print("Conexão verificada com sucesso.")

driver.close()
```

> Observação: este método deve ser chamado **antes** de `driver.close()`.

### 13.3 `driver.execute_query()`

Em versões mais recentes da biblioteca Neo4j, há o método `execute_query()`, que simplifica a execução de consultas, pois cuida automaticamente de abrir e fechar sessões.

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri, auth=(user, password))

records, summary, keys = driver.execute_query(
    "MATCH (p:Pessoa) RETURN p.nome AS nome"
)

for record in records:
    print(record["p.nome"])

driver.close()
```

Esse método é bastante conveniente para scripts simples ou consultas rápidas.

### 13.4 `driver.close()`

Fecha o driver e libera todos os recursos associados à conexão com o banco de dados.

```python
from neo4j import GraphDatabase

driver = GraphDatabase.driver(uri, auth=(user, password))

# ... uso normal do driver ...

driver.close()  # encerra a conexão com o Neo4j
```

Depois de `driver.close()`, qualquer tentativa de usar o driver (por exemplo, abrindo nova sessão) resultará em erro.

---

## 14) Referência ao uso de IA na documentação do projeto

### 14.1 Como o texto gerado pela IA foi usado

Para a elaboração da seção 11 (métodos da classe `Driver`), foi utilizada uma ferramenta de IA (ChatGPT, da OpenAI).  
A ferramenta foi utilizada para:

- Listar e explicar os principais métodos da classe `Driver`,
- Fornecer exemplos de código em Python,
- Auxiliar na redação em linguagem clara e organizada.

Todo o texto retornado pela IA foi **revisado e adaptado** pelos autores do trabalho antes de ser incluído na documentação.

Um possível texto para ser incluído na seção de metodologia é:

> Parte das explicações sobre os métodos da classe `Driver` da biblioteca Neo4j para Python foi elaborada com apoio da ferramenta de inteligência artificial ChatGPT, desenvolvida pela OpenAI. O conteúdo gerado foi revisado criticamente antes de sua inclusão na documentação.

### 14.2 Referência formal ao uso de IA

Na seção de referências, a ferramenta de IA pode ser mencionada da seguinte forma (formato próximo ao ABNT):

```text
OPENAI. ChatGPT – modelo de linguagem para geração de texto.
Ferramenta utilizada para apoio na descrição dos métodos da classe Driver
da biblioteca Neo4j em Python. Acesso em: nov. 2025.
```

No corpo do texto, a citação pode aparecer como:

> (OPENAI, 2025)

Dessa forma, o uso da IA fica **transparente e devidamente creditado** na documentação do projeto.
---