from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("NEO4J_URI")
user = os.getenv("NEO4J_USER")
password = os.getenv("NEO4J_PASSWORD")
database = os.getenv("NEO4J_DATABASE")

driver = GraphDatabase.driver(uri, auth=(user, password))

driver.verify_connectivity()

with driver.session(database="neo4j") as session:
    result = session.run("MATCH (p:Pessoa) RETURN p.nome AS nome")
    for record in result:
        print(record["nome"])

driver.close()
