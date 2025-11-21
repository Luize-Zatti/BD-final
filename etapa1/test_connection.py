from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE")

driver = GraphDatabase.driver(uri, auth=(user, password))

def test_db(tx):
    return tx.run("RETURN 'Conexão bem-sucedida!' AS msg").single()["msg"]

with driver.session(database=database) as session:
    print(session.execute_write(test_db))

driver.close()
