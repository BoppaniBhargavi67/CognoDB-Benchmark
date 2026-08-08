import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/database_comparison.csv")

pivot = df.pivot(
    index="query",
    columns="database",
    values="average"
)

pivot.plot(kind="bar", figsize=(12, 6))

plt.ylabel("Average Latency (ms)")
plt.xlabel("Query")
plt.title("Database Benchmark Comparison")
plt.xticks(rotation=0)
plt.legend(title="Database")
plt.tight_layout()

plt.savefig("results/database_comparison.png", dpi=300)

print("Comparison chart saved to results/database_comparison.png")