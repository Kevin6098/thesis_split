# scripts/preview_representative_comments.py
import argparse, random, textwrap
from pathlib import Path
import pandas as pd
from src.topic_inspection import summarise_cluster   # already exists

def main(slug, max_chars=120):
    df = pd.read_parquet(Path("data/processed") / f"{slug}_with_clusters.parquet",
                         columns=["cluster", "comment", "clean_joined"])
    for cid in sorted(df["cluster"].unique()):
        phrases, examples = summarise_cluster(df, cid, n_samples=3)
        words = ", ".join(w for w, _ in phrases)
        print(f"\n=== Cluster {cid:02d}  top words: {words}")
        for c in examples["comment"]:
            # scripts/preview_representative_comments.py 15 行目付近
            print("•", textwrap.shorten(c.replace("\n", " "),
                                        width=max_chars,
                                        placeholder="…"))
if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", required=True, choices=["high_rating","most_commented"])
    args = ap.parse_args()
    main(args.set)