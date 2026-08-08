from arango import ArangoClient
import random
import time
import csv
import os

client = ArangoClient(hosts="http://localhost:8529")
db = client.db("benchmark", username="root", password="benchmark")

sample_ids = random.sample(range(22470), 100)

results = []

queries = {
    "point_lookup": """
        FOR n IN pages
        FILTER n.id == @id
        RETURN n
    """,

    "one_hop": """
        FOR e IN links
        FILTER e._from == CONCAT("pages/", @id)
        RETURN e._to
    """,

    "two_hop": """
        FOR e1 IN links
        FILTER e1._from == CONCAT("pages/", @id)
        FOR e2 IN links
        FILTER e2._from == e1._to
        RETURN e2._to
    """,

    "three_hop": """
        FOR e1 IN links
        FILTER e1._from == CONCAT("pages/", @id)
        FOR e2 IN links
        FILTER e2._from == e1._to
        FOR e3 IN links
        FILTER e3._from == e2._to
        RETURN e3._to
    """,

    "aggregation": """
        RETURN LENGTH(
            FOR n IN pages
            RETURN n
        )
    """
}

print("Warm-up...")

for _ in range(10):
    db.aql.execute(
        queries["point_lookup"],
        bind_vars={"id": random.choice(sample_ids)}
    )

print("Running benchmarks...")

for query_name, query in queries.items():

    print(f"Benchmarking {query_name}...")

    for node_id in sample_ids:

        start = time.perf_counter()

        if query_name == "aggregation":
            cursor = db.aql.execute(query)
        else:
            cursor = db.aql.execute(
                query,
                bind_vars={"id": node_id}
            )

        list(cursor)

        end = time.perf_counter()

        results.append([
            query_name,
            node_id,
            (end - start) * 1000
        ])

os.makedirs("results", exist_ok=True)

output_file = "results/arangodb_results.csv"

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