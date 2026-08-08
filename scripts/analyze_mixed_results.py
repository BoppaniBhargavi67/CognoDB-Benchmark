import pandas as pd
import glob
import os

files = glob.glob("results/*_mixed_results.csv")

rows = []

for file in files:
    df = pd.read_csv(file)
    rows.append(df.iloc[0])

summary = pd.DataFrame(rows)

summary = summary.sort_values(
    "qps",
    ascending=False
)

print("\nMixed Workload Summary:")
print(
    summary[
        [
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
        ]
    ].to_string(index=False)
)

output = "results/mixed_workload_summary.csv"

summary.to_csv(
    output,
    index=False
)

print(f"\nSaved to {output}")
