# scripts/export_negative.py
from pathlib import Path
import pandas as pd

slug = "high_rating"
sent = pd.read_parquet(Path("data/processed") / f"{slug}_sentiment.parquet")
neg = sent[sent["sentiment_label"] == "negative"][["id","comment","clean_joined"]]
neg.to_csv(f"data/processed/{slug}_negative_reviews.csv", index=False)
print(f"✅ Exported {len(neg)} negative reviews to CSV")