from falkordb import FalkorDB
import csv
import time

DB_NAME = "benchmark"
FILE_PATH = "datasets/raw/facebook_large/musae_facebook_edges.csv"
BATCH_SIZE = 20000

db = FalkorDB(host="localhost", port=6379)
graph = db.select_graph(DB_NAME)

with open(FILE_PATH, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = [
        {
            "id_1": int(row["id_1"]),
            "id_2": int(row["id_2"])
        }
        for row in reader
    ]

print(f"Relationships to process: {len(rows)}")
print("Starting relationship load timing...")

start = time.perf_counter()

for i in range(0, len(rows), BATCH_SIZE):

    batch = rows[i:i + BATCH_SIZE]

    graph.query(
        """
        UNWIND $rows AS row
        MATCH (a:Page {id: row.id_1})
        MATCH (b:Page {id: row.id_2})
        MERGE (a)-[:LINKS_TO]->(b)
        """,
        {"rows": batch}
    )

    print(f"Processed {min(i + BATCH_SIZE, len(rows))} / {len(rows)}")

end = time.perf_counter()

elapsed = end - start
relationships_per_sec = len(rows) / elapsed

print("\nRelationship Load Result")
print("------------------------")
print(f"Relationships: {len(rows)}")
print(f"Load time: {elapsed:.3f} seconds")
print(f"Relationships/sec: {relationships_per_sec:.2f}")

result = graph.query(
    "MATCH ()-[r:LINKS_TO]->() RETURN count(r) AS total"
).result_set

print(f"Verified relationships in database: {result[0][0]}")
