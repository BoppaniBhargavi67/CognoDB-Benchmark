from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(os.getenv("COGNODB_USERNAME"), os.getenv("COGNODB_PASSWORD"))
)

with driver.session() as session:
    print("Nodes:",
          session.run("MATCH (n) RETURN count(n) AS c").single()["c"])

    print("Relationships:",
          session.run("MATCH ()-[r]->() RETURN count(r) AS c").single()["c"])

driver.close()