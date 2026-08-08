from neo4j import GraphDatabase
from dotenv import load_dotenv
import pandas as pd
import os

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(os.getenv("COGNODB_USERNAME"), os.getenv("COGNODB_PASSWORD"))
)

nodes = pd.read_csv(
    "datasets/raw/facebook_large/musae_facebook_target.csv"
)

node_list = nodes.to_dict("records")

query = """
UNWIND $rows AS row
MERGE (p:Page {id: row.id})
SET
    p.facebook_id = row.facebook_id,
    p.page_name = row.page_name,
    p.page_type = row.page_type
"""

batch_size = 100

with driver.session() as session:
    for i in range(0, len(node_list), batch_size):
        batch = node_list[i:i + batch_size]

        session.run(query, rows=batch).consume()

        if (i // batch_size) % 10 == 0:
            print(f"Inserted {min(i + batch_size, len(node_list))} / {len(node_list)}")

print("All nodes inserted successfully!")

driver.close()