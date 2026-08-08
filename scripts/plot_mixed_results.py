import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("results/mixed_workload_summary.csv")

# -----------------------------
# Throughput
# -----------------------------
plot = df.sort_values("qps", ascending=False)

plt.figure(figsize=(10, 6))
plt.bar(plot["database"], plot["qps"])

plt.ylabel("Throughput (queries/sec)")
plt.xlabel("Database")
plt.title("Mixed Workload - Throughput")
plt.tight_layout()

plt.savefig(
    "results/mixed_throughput.png",
    dpi=300
)

plt.close()


# -----------------------------
# P50 latency
# -----------------------------
plot = df.sort_values("p50_ms")

plt.figure(figsize=(10, 6))
plt.bar(plot["database"], plot["p50_ms"])

plt.ylabel("P50 Latency (ms)")
plt.xlabel("Database")
plt.title("Mixed Workload - P50 Latency")
plt.tight_layout()

plt.savefig(
    "results/mixed_p50_latency.png",
    dpi=300
)

plt.close()


# -----------------------------
# P95 latency
# -----------------------------
plot = df.sort_values("p95_ms")

plt.figure(figsize=(10, 6))
plt.bar(plot["database"], plot["p95_ms"])

plt.ylabel("P95 Latency (ms)")
plt.xlabel("Database")
plt.title("Mixed Workload - P95 Latency")
plt.tight_layout()

plt.savefig(
    "results/mixed_p95_latency.png",
    dpi=300
)

plt.close()

print("Mixed workload charts generated:")
print("results/mixed_throughput.png")
print("results/mixed_p50_latency.png")
print("results/mixed_p95_latency.png")