# scripts/topic_sentiment.py
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

slug = "high_rating"
# load clusters+topics + sentiment
df = pd.read_parquet(Path("data/processed") / f"{slug}_with_clusters.parquet")
sent = pd.read_parquet(Path("data/processed") / f"{slug}_sentiment.parquet")
df = df.merge(sent[["id","sentiment_score"]], on="id")

# average by dominant_topic
topic_avg = df.groupby("dominant_topic")["sentiment_score"]\
              .mean().sort_index()

plt.figure(figsize=(6,4))
topic_avg.plot.bar(color="salmon")
plt.ylabel("Avg. negative score")
plt.xlabel("LDA Topic ID")
plt.title(f"Avg. sentiment by topic ({slug})")
plt.tight_layout()
plt.savefig(f"data/processed/{slug}_topic_sentiment.png", dpi=200)
print("✅ Saved topic sentiment bar chart")