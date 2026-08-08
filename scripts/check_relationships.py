from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(os.getenv("COGNODB_USERNAME"), os.getenv("COGNODB_PASSWORD"))
)

with driver.session(database="neo4j") as session:
    result = session.run("""
        MATCH ()-[r]->()
        RETURN type(r) AS type, count(r) AS total
    """)

    for row in result:
        print(row["type"], row["total"])

driver.close()