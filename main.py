# main.py
# -------------------------------------
from argparse import ArgumentParser
from pathlib import Path
import pandas as pd

from src import config
from src.data_collection    import load_raw
from src.text_cleaning      import cleanse_dataframe
from src.vectorize          import build_tfidf
from src.cluster_eval       import best_k_silhouette
from src.clustering         import fit_kmeans
from src.topic_inspection   import summarise_cluster
from src.visualization      import plot_cluster_distribution, plot_top_ngrams
from src.sentiment_analysis import save_sentiment
from src.lda_modeling       import fit_lda, display_topics

STAGES = {
    "clean", 
    "cluster", 
    "topics", 
    "viz", 
    "sentiment", 
    "lda"
}

def run(slug: str, stage: str):
    # Stage: clean → produce cleaned text
    if stage == "clean":
        df = load_raw(config.DATASETS[slug])
        df = cleanse_dataframe(df, text_col="comment")
        out = config.DATA_DIR / "processed" / f"{slug}_clean_text.parquet"
        df.to_parquet(out, index=False)
        print(f"✔ Clean text saved to {out}")
        return

    # For all other stages, load the cleaned text
    clean_path = config.DATA_DIR / "processed" / f"{slug}_clean_text.parquet"
    if not clean_path.exists():
        raise FileNotFoundError(f"Run --stage clean first (no file at {clean_path})")
    df = pd.read_parquet(clean_path)

    if stage == "cluster":
        X, _      = build_tfidf(df)
        best_k, _ = best_k_silhouette(X)
        km        = fit_kmeans(X, best_k, config.MODEL_DIR / f"{slug}_kmeans_k{best_k}.pkl")
        df["cluster"] = km.labels_
        out = config.DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        df.to_parquet(out, index=False)
        print(f"✔ Clustering done (k={best_k}), saved to {out}")
        return

    if stage == "topics":
        clustered_path = config.DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        df = pd.read_parquet(clustered_path)
        for cid in sorted(df["cluster"].unique()):
            phrases, _ = summarise_cluster(df, cid)
            print(f"\nCluster {cid}:")
            for phr, cnt in phrases:
                print(f"  {phr}: {cnt}")
        return

    if stage == "viz":
        proc = config.DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        plot_cluster_distribution(proc)
        # Optionally: loop through clusters to plot top n-grams per cluster
        return

    if stage == "sentiment":
        scored_path = save_sentiment(df, slug)
        print(f"✔ Sentiment scored & saved to {scored_path}")
        return

    if stage == "lda":
        lda, vec = fit_lda(df, n_topics=8, model_path=config.MODEL_DIR / f"{slug}_lda.pkl")
        display_topics(lda, vec)
        return

def main():
    p = ArgumentParser()
    p.add_argument(
        "--set", choices=config.DATASETS.keys(), required=True,
        help="Which dataset to process (high_rating | most_commented)"
    )
    p.add_argument(
        "--stage", choices=STAGES, default="clean",
        help="Pipeline stage: clean, cluster, topics, viz, sentiment, lda"
    )
    args = p.parse_args()
    run(args.set, args.stage)

if __name__ == "__main__":
    main()
    