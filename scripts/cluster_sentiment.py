# scripts/cluster_sentiment.py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

slug = "high_rating"  # or "most_commented"
# 1) load the data WITH both cluster and sentiment columns
df = pd.read_parquet(Path("data/processed") / f"{slug}_with_clusters.parquet")
sent = pd.read_parquet(Path("data/processed") / f"{slug}_sentiment.parquet")

# join on id (or on index if they align)
df = df.merge(sent[["id","sentiment_score"]], on="id")

# 2) group & average
cluster_avg = df.groupby("cluster")["sentiment_score"].mean().sort_index()

# 3) plot
plt.figure(figsize=(6,4))
cluster_avg.plot.bar()
plt.ylabel("Avg. negative score")
plt.title(f"Avg. sentiment by cluster ({slug})")
plt.tight_layout()
plt.savefig(f"data/processed/{slug}_cluster_sentiment.png", dpi=200)
print("✅ Saved cluster sentiment bar chart")