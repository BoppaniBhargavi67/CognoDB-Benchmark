import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/percentile_summary.csv")

# Remove indexed variants because the main comparison
# should contain the five databases using the same query set.
df = df[~df["database"].str.endswith("_indexed")]

# -----------------------------
# Average latency
# -----------------------------
pivot = df.pivot(
    index="query",
    columns="database",
    values="average"
)

pivot.plot(kind="bar", figsize=(12, 6))

plt.ylabel("Average Latency (ms)")
plt.xlabel("Query")
plt.title("Database Comparison - Average Latency")
plt.xticks(rotation=0)
plt.legend(title="Database")
plt.tight_layout()

plt.savefig(
    "results/database_average_latency.png",
    dpi=300
)

plt.close()


# -----------------------------
# P50 latency
# -----------------------------
pivot = df.pivot(
    index="query",
    columns="database",
    values="p50"
)

pivot.plot(kind="bar", figsize=(12, 6))

plt.ylabel("P50 Latency (ms)")
plt.xlabel("Query")
plt.title("Database Comparison - P50 Latency")
plt.xticks(rotation=0)
plt.legend(title="Database")
plt.tight_layout()

plt.savefig(
    "results/database_p50_latency.png",
    dpi=300
)

plt.close()


# -----------------------------
# P95 latency
# -----------------------------
pivot = df.pivot(
    index="query",
    columns="database",
    values="p95"
)

pivot.plot(kind="bar", figsize=(12, 6))

plt.ylabel("P95 Latency (ms)")
plt.xlabel("Query")
plt.title("Database Comparison - P95 Latency")
plt.xticks(rotation=0)
plt.legend(title="Database")
plt.tight_layout()

plt.savefig(
    "results/database_p95_latency.png",
    dpi=300
)

plt.close()

print("Charts generated successfully:")
print("results/database_average_latency.png")
print("results/database_p50_latency.png")
print("results/database_p95_latency.png")