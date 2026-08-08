from neo4j import GraphDatabase
from dotenv import load_dotenv
import pandas as pd
import os

# Load environment variables
load_dotenv()

# Connect to CognoDB
driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(os.getenv("COGNODB_USERNAME"), os.getenv("COGNODB_PASSWORD"))
)

# Read relationships dataset
edges = pd.read_csv(
    "datasets/raw/facebook_large/musae_facebook_edges.csv"
)

edge_list = edges.to_dict("records")

# Cypher query
query = """
UNWIND $rows AS row

MATCH (a:Page {id: row.id_1})
MATCH (b:Page {id: row.id_2})

MERGE (a)-[:LINKS_TO]->(b)
"""

# Settings
batch_size = 5000
start = int(input("Enter resume position (0 for fresh run): "))

for i in range(start, len(edge_list), batch_size):

    batch = edge_list[i:i + batch_size]

    try:
        with driver.session() as session:
            session.run(query, rows=batch).consume()

        print(f"Inserted {min(i + batch_size, len(edge_list))} / {len(edge_list)}")

    except Exception as e:
        print("\nConnection lost!")
        print(f"Resume from: {i}")
        print(e)
        break

driver.close()

print("Script finished.")