import os

import psycopg2
from psycopg2.extras import RealDictCursor
import redis
from dotenv import load_dotenv

load_dotenv()

# PostgreSQL
PG_HOST = os.getenv("PG_HOST", "localhost")
PG_PORT = int(os.getenv("PG_PORT", "5432"))
PG_DB = os.getenv("PG_DB", "trabalho_bd2")
PG_USER = os.getenv("PG_USER", "postgres")
PG_PASSWORD = os.getenv("PG_PASSWORD", "")

# Redis
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", "6379"))
REDIS_DB = int(os.getenv("REDIS_DB", "0"))

def get_pg_connection():
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        dbname=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD,
    )
    return conn


def get_redis_connection():
    r = redis.Redis(
        host=REDIS_HOST,
        port=REDIS_PORT,
        db=REDIS_DB,
        decode_responses=True 
    )
    return r


def create_table():
    """Cria a tabela pessoas, se ainda não existir."""
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS pessoas (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            idade INT
        );
        """
    )
    conn.commit()
    cur.close()
    conn.close()
    print("[PostgreSQL] Tabela 'pessoas' criada (ou já existia).")


def create_person(nome: str, idade: int) -> int:
    """INSERT (CREATE): insere uma nova pessoa e retorna o id gerado."""
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO pessoas (nome, idade) VALUES (%s, %s) RETURNING id;",
        (nome, idade),
    )
    pessoa_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    print(f"[PostgreSQL] Pessoa criada com id={pessoa_id}.")
    return pessoa_id


def read_person(pessoa_id: int):
    """SELECT (READ): busca uma pessoa pelo id."""
    conn = get_pg_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "SELECT id, nome, idade FROM pessoas WHERE id = %s;",
        (pessoa_id,),
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    print(f"[PostgreSQL] Consulta pessoa id={pessoa_id} -> {row}")
    return row


def update_person(pessoa_id: int, novo_nome: str, nova_idade: int):
    """UPDATE: atualiza nome e idade da pessoa."""
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE pessoas SET nome = %s, idade = %s WHERE id = %s;",
        (novo_nome, nova_idade, pessoa_id),
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"[PostgreSQL] Pessoa id={pessoa_id} atualizada.")


def delete_person(pessoa_id: int):
    """DELETE: exclui a pessoa pelo id."""
    conn = get_pg_connection()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM pessoas WHERE id = %s;",
        (pessoa_id,),
    )
    conn.commit()
    cur.close()
    conn.close()
    print(f"[PostgreSQL] Pessoa id={pessoa_id} excluída.")


def redis_create_person_name(r, pessoa_id: int, nome: str):
    """
    grava o nome da pessoa em uma chave.
    """
    key = f"pessoa:{pessoa_id}:nome"
    r.set(key, nome)
    print(f"[Redis] SET {key} = {nome}")


def redis_read_person_name(r, pessoa_id: int):
    """
    lê o nome armazenado para a pessoa.
    """
    key = f"pessoa:{pessoa_id}:nome"
    value = r.get(key)
    print(f"[Redis] GET {key} -> {value}")
    return value


def redis_update_person_name(r, pessoa_id: int, novo_nome: str):
    """
    como é chave-valor, o update é simplesmente sobrescrever o valor.
    """
    key = f"pessoa:{pessoa_id}:nome"
    r.set(key, novo_nome)
    print(f"[Redis] UPDATE {key} = {novo_nome}")


def redis_delete_person_name(r, pessoa_id: int):
    """
    remove a chave associada ao nome da pessoa.
    """
    key = f"pessoa:{pessoa_id}:nome"
    r.delete(key)
    print(f"[Redis] DEL {key}")



if __name__ == "__main__":
    print("=== INÍCIO DO EXEMPLO CRUD PostgreSQL + Redis (.env) ===")

    create_table()
    r = get_redis_connection()

    print("\n--- CREATE ---")
    pessoa_id = create_person("Ana", 25)          
    redis_create_person_name(r, pessoa_id, "Ana") 

    print("\n--- READ ---")
    pessoa_pg = read_person(pessoa_id)
    pessoa_nome_redis = redis_read_person_name(r, pessoa_id)

    print("\n--- UPDATE ---")
    update_person(pessoa_id, "Ana Maria", 26)          
    redis_update_person_name(r, pessoa_id, "Ana Maria")

    print("\n--- READ após UPDATE ---")
    pessoa_pg = read_person(pessoa_id)
    pessoa_nome_redis = redis_read_person_name(r, pessoa_id)

    print("\n--- DELETE ---")
    delete_person(pessoa_id)                
    redis_delete_person_name(r, pessoa_id)  

    print("\n--- READ após DELETE ---")
    pessoa_pg = read_person(pessoa_id)
    pessoa_nome_redis = redis_read_person_name(r, pessoa_id)
