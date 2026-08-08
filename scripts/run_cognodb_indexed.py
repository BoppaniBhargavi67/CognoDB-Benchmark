from neo4j import GraphDatabase
from dotenv import load_dotenv
from benchmark_queries import QUERIES
import os
import csv
import random
import time

load_dotenv()

DB_NAME = "cognodb"

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(
        os.getenv("COGNODB_USERNAME"),
        os.getenv("COGNODB_PASSWORD")
    )
)

sample_ids = random.sample(range(22470), 100)

page_types = [
    "tvshow",
    "government",
    "company"
]

results = []

with driver.session() as session:

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
