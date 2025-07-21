#!/usr/bin/env python
"""
Create a line chart of topic prevalence (share of reviews)
for both corpora and save it to data/processed/topic_prevalence_lines.png

Usage
-----
    python scripts/topic_prevalence_plot.py          # default top 8 topics
    python scripts/topic_prevalence_plot.py --top 10
"""

import argparse
from pathlib import Path

import pandas as pd
import matplotlib
matplotlib.use("Agg")          # head-less backend
import matplotlib.pyplot as plt


def prevalence(path: Path) -> pd.Series:
    """Return Series index=topic_id, value=percentage (0-100)."""
    df = pd.read_parquet(path, columns=["dominant_topic"])
    pct = (
        df["dominant_topic"]
        .value_counts(normalize=True)
        .sort_index()
        .mul(100)
        .round(2)
    )
    return pct


def main(top_n: int):
    proc_dir = Path("data/processed")
    proc_dir.mkdir(parents=True, exist_ok=True)

    paths = {
        "High-Rating":    proc_dir / "high_rating_with_clusters.parquet",
        "Most-Commented": proc_dir / "most_commented_with_clusters.parquet",
    }

    # --- sanity check
    for label, p in paths.items():
        if not p.exists():
            raise SystemExit(f"❌ {p} not found – run LDA stage first.")

    # --- load
    hr = prevalence(paths["High-Rating"])
    mc = prevalence(paths["Most-Commented"])

    # align indices (0..N-1)
    all_topics = sorted(set(hr.index) | set(mc.index))[:top_n]
    hr = hr.reindex(all_topics, fill_value=0)
    mc = mc.reindex(all_topics, fill_value=0)

    # --- plot
    plt.figure(figsize=(6, 4))
    plt.plot(all_topics, hr, marker="o", label="High-Rating")
    plt.plot(all_topics, mc, marker="o", label="Most-Commented")

    plt.xticks(all_topics)
    plt.xlabel("LDA Topic ID")
    plt.ylabel("Prevalence (%)")
    plt.title("Topic Prevalence Comparison")
    plt.legend()
    plt.tight_layout()

    out = proc_dir / "topic_prevalence_lines.png"
    plt.savefig(out, dpi=300)
    plt.close()
    print("✅ PNG saved to", out.resolve())


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=8,
                    help="number of topics on X-axis (default=8)")
    args = ap.parse_args()
    main(args.top)