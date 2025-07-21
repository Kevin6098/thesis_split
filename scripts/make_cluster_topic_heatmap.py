"""
Generate a heatmap of K-means cluster × LDA dominant-topic distribution.

Usage:
    python scripts/make_cluster_topic_heatmap.py --set high_rating
    python scripts/make_cluster_topic_heatmap.py --set most_commented
"""

import argparse
from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib

matplotlib.use("Agg")          # GUI不要で PNG を保存
import matplotlib.pyplot as plt
from joblib import load        # LDA / Vectorizer ロード用


def ensure_dominant_topic(df: pd.DataFrame, slug: str) -> pd.DataFrame:
    """dominant_topic 列が無ければ LDA をロードして付与する"""
    if "dominant_topic" in df.columns:
        return df

    print("ℹ️  No dominant_topic column – computing on the fly…")
    model_dir = Path("models")
    lda_path   = model_dir / f"{slug}_lda.pkl"

    if not lda_path.exists():
        raise FileNotFoundError(f"{lda_path} not found. "
                                "Run stage lda first or place the model here.")

    lda, vec = load(lda_path)
    X = vec.transform(df["clean_joined"])
    df = df.copy()
    df["dominant_topic"] = lda.transform(X).argmax(axis=1)
    return df


def build_heatmap(slug: str):
    proc_dir = Path("data/processed")
    parquet = proc_dir / f"{slug}_with_clusters.parquet"

    if not parquet.exists():
        raise FileNotFoundError(
            f"{parquet} not found. Run the cluster stage first."
        )

    df = pd.read_parquet(parquet)
    df = ensure_dominant_topic(df, slug)

    # クロス集計（行: cluster, 列: dominant_topic）
    ct = pd.crosstab(
        df["cluster"],
        df["dominant_topic"],
        normalize="index"
    ).round(2)

    # 描画
    plt.figure(figsize=(8, 6))
    sns.heatmap(
        ct,
        annot=True,
        cmap="Blues",
        fmt=".2f",
        cbar_kws={"label": "Proportion"}
    )
    plt.xlabel("LDA Topic ID")
    plt.ylabel("K-means Cluster ID")
    plt.title(f"Cluster × Topic Distribution  ({slug})")
    plt.tight_layout()

    out = proc_dir / f"{slug}_cluster_topic_heatmap.png"
    plt.savefig(out, dpi=300)
    plt.close()
    print(f"✅ Saved: {out}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--set",
        required=True,
        choices=["high_rating", "most_commented"],
        help="which corpus to load"
    )
    args = parser.parse_args()

    build_heatmap(args.set)