from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(
        os.getenv("COGNODB_USERNAME"),
        os.getenv("COGNODB_PASSWORD")
    )
)

with driver.session(database="neo4j") as session:
    nodes = session.run(
        "MATCH (n) RETURN count(n) AS total"
    ).single()["total"]

    relationships = session.run(
        "MATCH ()-[r]->() RETURN count(r) AS total"
    ).single()["total"]

    print("Nodes:", nodes)
    print("Relationships:", relationships)

driver.close()