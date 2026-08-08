import pandas as pd

nodes = pd.read_csv("datasets/raw/facebook_large/musae_facebook_target.csv")
edges = pd.read_csv("datasets/raw/facebook_large/musae_facebook_edges.csv")

print("="*50)
print("Dataset Loaded Successfully")
print("="*50)

print(f"Total Nodes: {len(nodes)}")
print(f"Total Relationships: {len(edges)}")

print("\nNode Columns:")
print(nodes.columns)

print("\nRelationship Columns:")
print(edges.columns)

print("\nFirst 5 Nodes")
print(nodes.head())

print("\nFirst 5 Relationships")
print(edges.head())