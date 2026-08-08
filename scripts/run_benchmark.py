from neo4j import GraphDatabase
from dotenv import load_dotenv
from benchmark_queries import QUERIES
import os
import csv
import random
import time

load_dotenv()

DB_NAME = "memgraph"

driver = GraphDatabase.driver(
    os.getenv("COGNODB_URI"),
    auth=(
        os.getenv("COGNODB_USERNAME"),
        os.getenv("COGNODB_PASSWORD")
    )
)

sample_ids = random.sample(range(22470), 100)

results = []

with driver.session() as session:

    print("Warm-up...")

    for _ in range(10):
        session.run(
            QUERIES["point_lookup"],
            id=random.choice(sample_ids)
        ).consume()

    print("Running benchmarks...")

    for query_name, query in QUERIES.items():

        print(f"Benchmarking {query_name}...")

        for node_id in sample_ids:

            start = time.perf_counter()

            if query_name == "aggregation":
                session.run(query).consume()
            else:
                session.run(query, id=node_id).consume()

            end = time.perf_counter()

            results.append([
                query_name,
                node_id,
                (end - start) * 1000
            ])

driver.close()

os.makedirs("results", exist_ok=True)

output_file = f"results/{DB_NAME}_results.csv"



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