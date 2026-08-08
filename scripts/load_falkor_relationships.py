from falkordb import FalkorDB
import csv

db = FalkorDB(host="localhost", port=6379)
graph = db.select_graph("benchmark")

file_path = "datasets/raw/facebook_large/musae_facebook_edges.csv"

with open(file_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Loading {len(rows)} relationships...")

batch_size = 5000

for start in range(0, len(rows), batch_size):
    batch = rows[start:start + batch_size]

    graph.query(
        """
        UNWIND $rows AS row
        MATCH (a:Page {id: row.id_1})
        MATCH (b:Page {id: row.id_2})
        MERGE (a)-[:LINKS_TO]->(b)
        """,
        {
            "rows": [
                {
                    "id_1": int(row["id_1"]),
                    "id_2": int(row["id_2"])
                }
                for row in batch
            ]
        }
    )

    print(f"Inserted {min(start + batch_size, len(rows))} / {len(rows)}")

print("Relationship loading finished.")