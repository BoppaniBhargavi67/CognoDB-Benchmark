from neo4j import GraphDatabase
from benchmark_queries import QUERIES
import csv
import random
import time
import os

DB_NAME = "neo4j"

driver = GraphDatabase.driver(
    "bolt://127.0.0.1:7687",
    auth=("neo4j", "neo4j1234")
)

page_types = [
    "tvshow",
    "government",
    "company"
]

results = []

with driver.session(database="neo4j") as session:

    print("Creating index...")

    session.run(
        """
        CREATE INDEX page_type_index IF NOT EXISTS
        FOR (p:Page) ON (p.page_type)
        """
    ).consume()

    print("Index ready.")

    print("Warm-up...")

    for _ in range(10):
        session.run(
            QUERIES["indexed_lookup"],
            page_type=random.choice(page_types)
        ).consume()

    print("Running indexed lookup benchmark...")

    for i in range(100):

        start = time.perf_counter()

        session.run(
            QUERIES["indexed_lookup"],
            page_type=random.choice(page_types)
        ).consume()

        end = time.perf_counter()

        results.append([
            "indexed_lookup",
            i,
            (end - start) * 1000
        ])

driver.close()

os.makedirs("results", exist_ok=True)

output_file = "results/neo4j_indexed_results.csv"

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