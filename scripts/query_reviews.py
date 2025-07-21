# scripts/query_reviews.py
import argparse, re
from pathlib import Path
import pandas as pd, textwrap

def main(slug, kw, n):
    df = pd.read_parquet(Path("data/processed")/f"{slug}_with_clusters.parquet",
                         columns=["cluster","title","comment"])
    pat = re.compile(kw, re.I)
    hits = df[df["comment"].str.contains(pat, na=False)].head(n)
    print(f"Found {len(hits)} reviews containing '{kw}':\n")
    for _, row in hits.iterrows():
        txt = textwrap.shorten(row.comment.replace("\n"," "), width=140, placeholder="…")
        print(f"[C{row.cluster}] {row.title} – {txt}")

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", required=True, choices=["high_rating","most_commented"])
    ap.add_argument("--kw", required=True, help="keyword / regex (JP ok)")
    ap.add_argument("--n", type=int, default=5)
    args = ap.parse_args()
    main(args.set, args.kw, args.n)