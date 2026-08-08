import pandas as pd

DB_NAME = "cognodb"

df = pd.read_csv(f"results/{DB_NAME}_results.csv")

summary = df.groupby("query")["latency_ms"].agg(
    average="mean",
    minimum="min",
    maximum="max",
    median="median",
    p95=lambda x: x.quantile(0.95)
)

print(summary)

summary.to_csv(f"results/{DB_NAME}_summary.csv", index=False)
print(f"\nSummary saved to results/{DB_NAME}_summary.csv")