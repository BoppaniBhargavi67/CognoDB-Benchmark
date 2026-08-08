from falkordb import FalkorDB
from benchmark_queries import QUERIES
import random
import time
import csv
import os

DB_NAME = "falkordb"

db = FalkorDB(host="localhost", port=6379)
graph = db.select_graph("benchmark")

sample_ids = random.sample(range(22470), 100)

page_types = [
    "tvshow",
    "government",
    "company"
]

results = []

print("Creating index...")

try:
    graph.query(
        "CREATE INDEX FOR (p:Page) ON (p.page_type)"
    )
    print("Index created.")
except Exception:
    print("Index already exists or could not be recreated.")

print("Warm-up...")

for _ in range(10):
    graph.query(
        QUERIES["point_lookup"],
        {"id": random.choice(sample_ids)}
    )

print("Running benchmarks...")

for query_name, query in QUERIES.items():

    print(f"Benchmarking {query_name}...")

    for node_id in sample_ids:

        start = time.perf_counter()

        if query_name == "aggregation":
            graph.query(query)

        elif query_name == "indexed_lookup":
            graph.query(
                query,
                {"page_type": random.choice(page_types)}
            )

        else:
            graph.query(
                query,
                {"id": node_id}
            )

        end = time.perf_counter()

        results.append([
            query_name,
            node_id,
            (end - start) * 1000
        ])

os.makedirs("results", exist_ok=True)

output_file = f"results/{DB_NAME}_indexed_results.csv"

with open(output_file, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "query",
        "node_id",
        "latency_ms"
    ])

    writer.writerows(results)

print("\nBenchmark completed!")
print(f"Results saved to {output_file}")