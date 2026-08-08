from neo4j import GraphDatabase
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import os
import random
import time
import csv

load_dotenv()

DB_NAME = os.getenv("BENCHMARK_DB", "neo4j")
URI = os.getenv("BENCHMARK_URI", "bolt://127.0.0.1:7687")
USERNAME = os.getenv("BENCHMARK_USERNAME", "neo4j")
PASSWORD = os.getenv("BENCHMARK_PASSWORD", "neo4j1234")

CLIENTS = 10
DURATION = 30
READ_RATIO = 0.8

sample_ids = random.sample(range(22470), 100)

READ_QUERIES = [
    ("point_lookup",
     "MATCH (p:Page {id: $id}) RETURN p"),

    ("one_hop",
     "MATCH (p:Page {id: $id})-[:LINKS_TO]->(n) "
     "RETURN count(n) AS neighbors"),

    ("two_hop",
     "MATCH (p:Page {id: $id})-[:LINKS_TO]->()-[:LINKS_TO]->(n) "
     "RETURN count(n) AS neighbors"),

    ("three_hop",
     "MATCH (p:Page {id: $id})"
     "-[:LINKS_TO]->()-[:LINKS_TO]->()-[:LINKS_TO]->(n) "
     "RETURN count(n) AS neighbors"),

    ("aggregation",
     "MATCH (p:Page) "
     "RETURN p.page_type AS page_type, count(*) AS total")
]

WRITE_QUERY = """
CREATE (p:BenchmarkTemp {id: $temp_id})
"""

DELETE_QUERY = """
MATCH (p:BenchmarkTemp {id: $temp_id})
DELETE p
"""


def worker(worker_id):
    driver = GraphDatabase.driver(
        URI,
        auth=(USERNAME, PASSWORD)
    )

    reads = 0
    writes = 0
    errors = 0
    latencies = []

    end_time = time.perf_counter() + DURATION

    try:
        with driver.session() as session:

            while time.perf_counter() < end_time:

                is_read = random.random() < READ_RATIO
                start = time.perf_counter()

                try:
                    if is_read:
                        name, query = random.choice(READ_QUERIES)

                        session.run(
                            query,
                            id=random.choice(sample_ids)
                        ).consume()

                        reads += 1

                    else:
                        temp_id = f"{worker_id}_{time.time_ns()}"

                        session.run(
                            WRITE_QUERY,
                            temp_id=temp_id
                        ).consume()

                        session.run(
                            DELETE_QUERY,
                            temp_id=temp_id
                        ).consume()

                        writes += 1

                    latencies.append(
                        (time.perf_counter() - start) * 1000
                    )

                except Exception:
                    errors += 1

    finally:
        driver.close()

    return reads, writes, errors, latencies


print(f"Database: {DB_NAME}")
print(f"Clients: {CLIENTS}")
print(f"Duration: {DURATION}s")
print(f"Read/Write mix: 80/20")

print("\nWarm-up...")

driver = GraphDatabase.driver(
    URI,
    auth=(USERNAME, PASSWORD)
)

with driver.session() as session:
    for _ in range(10):
        session.run(
            READ_QUERIES[0][1],
            id=random.choice(sample_ids)
        ).consume()

driver.close()

print("Running mixed workload...")

start = time.perf_counter()

with ThreadPoolExecutor(max_workers=CLIENTS) as executor:
    futures = [
        executor.submit(worker, i)
        for i in range(CLIENTS)
    ]

    results = [f.result() for f in futures]

elapsed = time.perf_counter() - start

reads = sum(r[0] for r in results)
writes = sum(r[1] for r in results)
errors = sum(r[2] for r in results)

latencies = [
    latency
    for r in results
    for latency in r[3]
]

total = reads + writes
qps = total / elapsed

latencies.sort()

p50 = latencies[int(len(latencies) * 0.50)]
p95 = latencies[int(len(latencies) * 0.95)]

print("\nMixed workload completed!")
print(f"Elapsed: {elapsed:.2f}s")
print(f"Total operations: {total}")
print(f"Reads: {reads}")
print(f"Writes: {writes}")
print(f"Errors: {errors}")
print(f"Throughput: {qps:.2f} queries/sec")
print(f"P50 latency: {p50:.3f} ms")
print(f"P95 latency: {p95:.3f} ms")

os.makedirs("results", exist_ok=True)

output = f"results/{DB_NAME}_mixed_results.csv"

with open(output, "w", newline="") as f:
    writer = csv.writer(f)

    writer.writerow([
        "database",
        "clients",
        "duration_sec",
        "read_ratio",
        "total_operations",
        "reads",
        "writes",
        "errors",
        "qps",
        "p50_ms",
        "p95_ms"
    ])

    writer.writerow([
        DB_NAME,
        CLIENTS,
        elapsed,
        READ_RATIO,
        total,
        reads,
        writes,
        errors,
        qps,
        p50,
        p95
    ])

print(f"Results saved to {output}")