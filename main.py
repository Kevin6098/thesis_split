# main.py
# -------------------------------------
from argparse import ArgumentParser
from pathlib import Path
import pandas as pd

from src import config
from src.data_collection    import load_raw
from src.text_cleaning      import cleanse_dataframe
from src.vectorize          import build_tfidf
from src.cluster_eval       import best_k_silhouette, fast_best_k_silhouette, parallel_best_k_silhouette
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

def run(slug: str, stage: str, use_sampling=True, sample_size=100000, use_parallel=False, n_jobs=-1):
    print(f"🚀 Starting pipeline for dataset: {slug}")
    print(f"📋 Stage: {stage}")
    if use_sampling:
        print(f"🎲 Using sampling (sample_size={sample_size:,}) for faster computation")
    if use_parallel:
        print(f"⚡ Using parallel processing ({n_jobs if n_jobs > 0 else 'all'} CPUs)")
    
    # Stage: clean → produce cleaned text
    if stage == "clean":
        print("📥 Loading raw data...")
        df = load_raw(config.DATASETS[slug])
        print(f"✅ Loaded {len(df):,} records")
        
        df = cleanse_dataframe(df, text_col="comment")
        out = config.DATA_DIR / "processed" / f"{slug}_clean_text.parquet"
        df.to_parquet(out, index=False)
        print(f"✅ Clean text saved to {out}")
        return

    # For all other stages, load the cleaned text
    clean_path = config.DATA_DIR / "processed" / f"{slug}_clean_text.parquet"
    if not clean_path.exists():
        raise FileNotFoundError(f"Run --stage clean first (no file at {clean_path})")
    
    print("📥 Loading cleaned data...")
    df = pd.read_parquet(clean_path)
    print(f"✅ Loaded {len(df):,} cleaned records")

    if stage == "cluster":
        print("🔍 Building TF-IDF vectors...")
        X, _ = build_tfidf(df)
        print(f"✅ TF-IDF built: {X.shape}")
        
        # Choose the appropriate k evaluation method
        if use_parallel:
            print("⚡ Using parallel k evaluation...")
            best_k, _ = parallel_best_k_silhouette(
                X, 
                k_min=2, 
                k_max=10, 
                sample_size=sample_size, 
                n_jobs=n_jobs
            )
        elif use_sampling:
            print("🎲 Using fast sampling-based k evaluation...")
            best_k, _ = fast_best_k_silhouette(
                X, 
                k_min=2, 
                k_max=10, 
                sample_size=sample_size
            )
        else:
            print("🔄 Using original k evaluation...")
            best_k, _ = best_k_silhouette(
                X, 
                k_min=2, 
                k_max=10, 
                use_sampling=False
            )
        
        print(f"🎯 Optimal k: {best_k}")
        
        # Perform clustering
        print("🔀 Performing clustering...")
        km = fit_kmeans(X, best_k, config.MODEL_DIR / f"{slug}_kmeans_k{best_k}.pkl")
        df["cluster"] = km.labels_
        out = config.DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        df.to_parquet(out, index=False)
        print(f"✅ Clustering done (k={best_k}), saved to {out}")
        return

    if stage == "topics":
        print("📊 Analyzing cluster topics...")
        clustered_path = config.DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        df = pd.read_parquet(clustered_path)
        for cid in sorted(df["cluster"].unique()):
            phrases, _ = summarise_cluster(df, cid)
            print(f"\nCluster {cid}:")
            for phr, cnt in phrases:
                print(f"  {phr}: {cnt}")
        return

    if stage == "viz":
        print("📈 Generating visualizations...")
        proc = config.DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        plot_cluster_distribution(proc)
        # Optionally: loop through clusters to plot top n-grams per cluster
        print("✅ Visualizations completed")
        return

    if stage == "sentiment":
        print("😊 Analyzing sentiment...")
        scored_path = save_sentiment(df, slug)
        print(f"✅ Sentiment scored & saved to {scored_path}")
        return

    if stage == "lda":
        print("📚 Fitting LDA model...")
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
    p.add_argument(
        "--no-sampling", action="store_true",
        help="Disable sampling (use full dataset for silhouette calculation)"
    )
    p.add_argument(
        "--sample-size", type=int, default=100000,
        help="Sample size for silhouette calculation (default: 100000)"
    )
    p.add_argument(
        "--parallel", action="store_true",
        help="Use parallel processing for k evaluation"
    )
    p.add_argument(
        "--n-jobs", type=int, default=-1,
        help="Number of parallel jobs (-1 for all CPUs)"
    )
    
    args = p.parse_args()
    
    run(
        args.set, 
        args.stage,
        use_sampling=not args.no_sampling,
        sample_size=args.sample_size,
        use_parallel=args.parallel,
        n_jobs=args.n_jobs
    )

if __name__ == "__main__":
    main()
    