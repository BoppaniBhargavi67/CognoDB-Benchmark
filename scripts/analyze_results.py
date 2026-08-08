import pandas as pd
import glob
import os

files = glob.glob("results/*_results.csv")

all_summaries = []

for file in files:
    df = pd.read_csv(file)

    if "query" not in df.columns or "latency_ms" not in df.columns:
        continue

    database = os.path.basename(file).replace("_results.csv", "")

    summary = df.groupby("query")["latency_ms"].agg(
        iterations="count",
        average="mean",
        minimum="min",
        maximum="max",
        p50="median",
        p95=lambda x: x.quantile(0.95)
    ).reset_index()

    summary.insert(0, "database", database)
    all_summaries.append(summary)

final = pd.concat(all_summaries, ignore_index=True)

final.to_csv("results/percentile_summary.csv", index=False)

print("\nPercentile Summary:")
print(final.to_string(index=False))
print("\nSaved to results/percentile_summary.csv")