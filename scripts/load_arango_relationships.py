from arango import ArangoClient
import csv

client = ArangoClient(hosts="http://localhost:8529")
db = client.db("benchmark", username="root", password="benchmark")

# Create edge collection
if not db.has_collection("links"):
    db.create_collection("links", edge=True)

links = db.collection("links")

file_path = "datasets/raw/facebook_large/musae_facebook_edges.csv"

with open(file_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Loading {len(rows)} relationships...")

batch_size = 5000

for start in range(0, len(rows), batch_size):

    batch = []

    for row in rows[start:start + batch_size]:
        batch.append({
            "_from": f"pages/{row['id_1']}",
            "_to": f"pages/{row['id_2']}"
        })

    links.insert_many(batch, overwrite=True)

    print(f"Inserted {min(start + batch_size, len(rows))} / {len(rows)}")

print("Relationship loading finished.")