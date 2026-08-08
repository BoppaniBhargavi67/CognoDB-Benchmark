import pandas as pd
import os

databases = [
    "cognodb",
    "neo4j",
    "memgraph",
    "falkordb",
    "arangodb"
]

frames = []

for db in databases:

    file = f"results/{db}_results.csv"

    df = pd.read_csv(file)

    summary = (
        df.groupby("query")["latency_ms"]
        .mean()
        .reset_index()
        .rename(columns={"latency_ms": "average"})
    )

    summary["database"] = db

    frames.append(summary)

comparison = pd.concat(frames, ignore_index=True)

comparison = comparison[
    ["database", "query", "average"]
]

comparison.to_csv(
    "results/database_comparison.csv",
    index=False
)

print("\nFinal comparison:")
print(comparison.to_string(index=False))

print("\nSaved to results/database_comparison.csv")