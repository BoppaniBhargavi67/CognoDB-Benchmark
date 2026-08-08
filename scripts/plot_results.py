import pandas as pd
import matplotlib.pyplot as plt
DB_NAME = "cognodb"

df = pd.read_csv(f"results/{DB_NAME}_summary.csv")

queries = [
    "aggregation",
    "one_hop",
    "point_lookup",
    "three_hop",
    "two_hop"
]

plt.figure(figsize=(8, 5))

plt.bar(queries, df["average"])

plt.xticks(rotation=45)
plt.ylabel("Average Latency (ms)")
plt.title(f"{DB_NAME.upper()} Benchmark Results")

plt.tight_layout()

plt.savefig(f"results/{DB_NAME}_benchmark.png")

print(f"Chart saved to results/{DB_NAME}_benchmark.png")