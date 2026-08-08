from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(os.getenv("COGNODB_USERNAME"), os.getenv("COGNODB_PASSWORD"))
)

with driver.session() as session:

    # Count before delete
    before = session.run(
        "MATCH (n) RETURN count(n) AS c"
    ).single()["c"]

    print("Before:", before)

    # Delete
    session.run("MATCH (n) DETACH DELETE n").consume()

    # Count after delete
    after = session.run(
        "MATCH (n) RETURN count(n) AS c"
    ).single()["c"]

    print("After:", after)

driver.close()