# src/visualization.py
# -------------------------------------
from __future__ import annotations
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def plot_cluster_distribution(processed_path: Path) -> None:
    """
    Bar chart of review‐volume per cluster.
    Expects a parquet with a 'cluster' column.
    """
    df = pd.read_parquet(processed_path)
    counts = df["cluster"].value_counts().sort_index()
    ax = counts.plot.bar(figsize=(8, 5), title="Review Volume by Cluster")
    ax.set_xlabel("Cluster ID")
    ax.set_ylabel("Number of Reviews")
    plt.tight_layout()
    plt.show()

def plot_top_ngrams(phrases: list[tuple[str, float]], title: str = "Top Phrases") -> None:
    """
    Horizontal bar chart of top n-grams.
    `phrases` is a list of (ngram, frequency).
    """
    words, freqs = zip(*phrases)
    plt.figure(figsize=(8, 5))
    plt.barh(words, freqs)
    plt.gca().invert_yaxis()
    plt.title(title)
    plt.xlabel("Frequency")
    plt.tight_layout()
    plt.show()