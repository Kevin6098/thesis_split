#!/usr/bin/env python
"""
Export top terms for each K-means cluster *and* each LDA topic.

Usage
-----
    python scripts/export_top_terms.py --set high_rating --top 15
    python scripts/export_top_terms.py --set most_commented --top 10

Outputs
-------
    data/processed/<slug>_cluster_top_terms.csv
    data/processed/<slug>_lda_top_terms.csv
"""

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from joblib import load
from sklearn.feature_extraction.text import CountVectorizer


# ----------------------------------------------------------------------
def cluster_top_terms(df: pd.DataFrame, top: int = 10) -> pd.DataFrame:
    """Return DataFrame[cluster, term, freq] with top terms per cluster."""
    rows = []
    for cid, sub in df.groupby("cluster"):
        vec = CountVectorizer(max_features=20_000, ngram_range=(1, 1))
        X   = vec.fit_transform(sub["clean_joined"])
        freqs = np.asarray(X.sum(axis=0)).ravel()
        vocab = np.array(vec.get_feature_names_out())
        top_idx = freqs.argsort()[::-1][:top]
        for term, f in zip(vocab[top_idx], freqs[top_idx]):
            rows.append({"cluster": cid, "term": term, "freq": int(f)})
    return pd.DataFrame(rows)


def lda_top_terms(model_path: Path, top: int = 10) -> pd.DataFrame:
    """Return DataFrame[topic, term, weight] with top terms per topic."""
    lda, vec = load(model_path)          # (LatentDirichletAllocation, CountVectorizer)
    vocab = np.array(vec.get_feature_names_out())
    rows  = []
    for tid, comp in enumerate(lda.components_):
        top_idx = comp.argsort()[::-1][:top]
        for term, w in zip(vocab[top_idx], comp[top_idx]):
            rows.append({"topic": tid, "term": term, "weight": float(w)})
    return pd.DataFrame(rows)


# ----------------------------------------------------------------------
def main(slug: str, top: int):
    proc_dir  = Path("data/processed")
    model_dir = Path("models")

    parquet    = proc_dir / f"{slug}_with_clusters.parquet"
    lda_pickle = model_dir / f"{slug}_lda.pkl"

    if not parquet.exists():
        raise FileNotFoundError(f"{parquet} not found – run cluster stage first.")
    if not lda_pickle.exists():
        raise FileNotFoundError(f"{lda_pickle} not found – run lda stage first.")

    # ---- cluster terms
    df = pd.read_parquet(parquet, columns=["cluster", "clean_joined"])
    cluster_terms = cluster_top_terms(df, top=top)
    c_out = proc_dir / f"{slug}_cluster_top_terms.csv"
    cluster_terms.to_csv(c_out, index=False)
    print(f"✅ saved {c_out}")

    # ---- lda terms
    lda_terms = lda_top_terms(lda_pickle, top=top)
    l_out = proc_dir / f"{slug}_lda_top_terms.csv"
    lda_terms.to_csv(l_out, index=False)
    print(f"✅ saved {l_out}")


# ----------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--set", required=True,
                        choices=["high_rating", "most_commented"],
                        help="corpus to process")
    parser.add_argument("--top", type=int, default=10,
                        help="how many terms per cluster/topic")
    args = parser.parse_args()

    main(args.set, args.top)