# show_sentiment.py
import pandas as pd
from pathlib import Path

# choose your corpus
slug = "high_rating"   # or "most_commented"

# load the scored parquet
path = Path("data/processed") / f"{slug}_sentiment.parquet"
df   = pd.read_parquet(path)

# 1) overall label counts
print("=== sentiment_label counts ===")
print(df["sentiment_label"].value_counts(), "\n")

# 2) basic score distribution
print("=== sentiment_score summary ===")
print(df["sentiment_score"].describe(), "\n")

# 3) (optional) average score by cluster
if "cluster" in df.columns:
    print("=== avg. sentiment_score by cluster ===")
    print(
      df.groupby("cluster")["sentiment_score"]
        .mean()
        .sort_index()
        .round(3)
    )