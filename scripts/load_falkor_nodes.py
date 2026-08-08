from falkordb import FalkorDB
import csv

db = FalkorDB(host="localhost", port=6379)
graph = db.select_graph("benchmark")

file_path = "datasets/raw/facebook_large/musae_facebook_target.csv"

with open(file_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    rows = list(reader)

print(f"Loading {len(rows)} nodes...")

for i, row in enumerate(rows, 1):
    graph.query(
        """
        MERGE (n:Page {
            id: $id,
            facebook_id: $facebook_id,
            page_name: $page_name,
            page_type: $page_type
        })
        """,
        {
            "id": int(row["id"]),
            "facebook_id": row["facebook_id"],
            "page_name": row["page_name"],
            "page_type": row["page_type"]
        }
    )

    if i % 1000 == 0 or i == len(rows):
        print(f"Inserted {i} / {len(rows)}")

print("Node loading finished.")