from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(os.getenv("COGNODB_USERNAME"), os.getenv("COGNODB_PASSWORD"))
)

with driver.session() as session:
    result = session.run("""
    MATCH (n)
    UNWIND labels(n) AS label
    RETURN label, count(*) AS cnt
    ORDER BY cnt DESC
    """)

    for row in result:
        print(row["label"], row["cnt"])

driver.close()