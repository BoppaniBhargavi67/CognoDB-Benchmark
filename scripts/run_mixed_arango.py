from arango import ArangoClient
from concurrent.futures import ThreadPoolExecutor
import random
import time
import csv
import os

DB_NAME = "arangodb"
CLIENTS = 10
DURATION = 30
READ_RATIO = 0.8

sample_ids = random.sample(range(22470), 100)

READ_QUERIES = [
    (
        "point_lookup",
        """
        FOR n IN pages
        FILTER n.id == @id
        RETURN n
        """
    ),
    (
        "one_hop",
        """
        FOR e IN links
        FILTER e._from == CONCAT("pages/", @id)
        RETURN e._to
        """
    ),
    (
        "two_hop",
        """
        FOR e1 IN links
        FILTER e1._from == CONCAT("pages/", @id)
        FOR e2 IN links
        FILTER e2._from == e1._to
        RETURN e2._to
        """
    ),
    (
        "three_hop",
        """
        FOR e1 IN links
        FILTER e1._from == CONCAT("pages/", @id)
        FOR e2 IN links
        FILTER e2._from == e1._to
        FOR e3 IN links
        FILTER e3._from == e2._to
        RETURN e3._to
        """
    ),
    (
        "aggregation",
        """
        RETURN LENGTH(
            FOR n IN pages
            RETURN n
        )
        """
    )
]


def worker(worker_id):
    client = ArangoClient(
        hosts="http://localhost:8529"
    )

    db = client.db(
        "benchmark",
        username="root",
        password="benchmark"
    )

    pages = db.collection("pages")

    reads = 0
    writes = 0
    errors = 0
    latencies = []

    end_time = time.perf_counter() + DURATION

    try:
        while time.perf_counter() < end_time:

            is_read = random.random() < READ_RATIO
            start = time.perf_counter()

            try:

                if is_read:

                    name, query = random.choice(
                        READ_QUERIES
                    )

                    if name == "aggregation":
                        cursor = db.aql.execute(query)
                    else:
                        cursor = db.aql.execute(
                            query,
                            bind_vars={
                                "id": random.choice(sample_ids)
                            }
                        )

                    list(cursor)

                    reads += 1

                else:

                    temp_key = (
                        f"bench_{worker_id}_"
                        f"{time.time_ns()}"
                    )

                    pages.insert({
                        "_key": temp_key,
                        "id": -1,
                        "page_name": "BenchmarkTemp",
                        "page_type": "temporary"
                    })

                    pages.delete(temp_key)

                    writes += 1

                latencies.append(
                    (time.perf_counter() - start) * 1000
                )

            except Exception as e:

                errors += 1

                if errors <= 5:
                    print(
                        f"Worker {worker_id} error: {e}"
                    )

    finally:
        client.close()

    return reads, writes, errors, latencies


print(f"Database: {DB_NAME}")
print(f"Clients: {CLIENTS}")
print(f"Duration: {DURATION}s")
print("Read/Write mix: 80/20")

client = ArangoClient(
    hosts="http://localhost:8529"
)

db = client.db(
    "benchmark",
    username="root",
    password="benchmark"
)

print("\nWarm-up...")

for _ in range(10):

    cursor = db.aql.execute(
        READ_QUERIES[0][1],
        bind_vars={
            "id": random.choice(sample_ids)
        }
    )

    list(cursor)

client.close()

print("Running mixed workload...")

start = time.perf_counter()

with ThreadPoolExecutor(
    max_workers=CLIENTS
) as executor:

    futures = [
        executor.submit(worker, i)
        for i in range(CLIENTS)
    ]

    results = [
        f.result()
        for f in futures
    ]

elapsed = time.perf_counter() - start

reads = sum(
    r[0] for r in results
)

writes = sum(
    r[1] for r in results
)

errors = sum(
    r[2] for r in results
)

latencies = [
    latency
    for r in results
    for latency in r[3]
]

total = reads + writes

qps = total / elapsed

latencies.sort()

p50 = latencies[
    int(len(latencies) * 0.50)
]

p95 = latencies[
    int(len(latencies) * 0.95)
]

print("\nMixed workload completed!")

print(
    f"Elapsed: {elapsed:.2f}s"
)

print(
    f"Total operations: {total}"
)

print(
    f"Reads: {reads}"
)

print(
    f"Writes: {writes}"
)

print(
    f"Errors: {errors}"
)

print(
    f"Throughput: {qps:.2f} queries/sec"
)

print(
    f"P50 latency: {p50:.3f} ms"
)

print(
    f"P95 latency: {p95:.3f} ms"
)

os.makedirs(
    "results",
    exist_ok=True
)

output = (
    "results/"
    f"{DB_NAME}_mixed_results.csv"
)

with open(
    output,
    "w",
    newline=""
) as f:

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

print(
    f"Results saved to {output}"
)