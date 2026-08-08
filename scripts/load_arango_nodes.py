from arango import ArangoClient
import csv

client = ArangoClient(hosts="http://localhost:8529")
db = client.db("_system", username="root", password="benchmark")

# Create benchmark database
if not db.has_database("benchmark"):
    db.create_database("benchmark")

db = client.db("benchmark", username="root", password="benchmark")

# Create node collection
if not db.has_collection("pages"):
    db.create_collection("pages")

pages = db.collection("pages")

file_path = "datasets/raw/facebook_large/musae_facebook_target.csv"

with open(file_path, newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    rows = list(reader)

print(f"Loading {len(rows)} nodes...")

batch_size = 5000

for start in range(0, len(rows), batch_size):

    batch = []

    for row in rows[start:start + batch_size]:
        batch.append({
            "_key": row["id"],
            "id": int(row["id"]),
            "facebook_id": row["facebook_id"],
            "page_name": row["page_name"],
            "page_type": row["page_type"]
        })

    pages.insert_many(batch, overwrite=True)

    print(f"Inserted {min(start + batch_size, len(rows))} / {len(rows)}")

print("Node loading finished.")