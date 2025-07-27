#!/usr/bin/env python
"""
Optimized main pipeline with parallel processing, sampling, and caching.
This version should run much faster than the original pipeline.
"""

from argparse import ArgumentParser
from pathlib import Path
import pandas as pd
import time
import multiprocessing as mp

from src import config
from src.data_collection import load_raw
from src.text_cleaning import cleanse_dataframe
from src.vectorize import build_tfidf
from src.optimized_clustering import optimized_best_k_silhouette, sample_based_k_selection
from src.clustering import fit_kmeans
from src.topic_inspection import summarise_cluster
from src.visualization import plot_cluster_distribution, plot_top_ngrams
from src.sentiment_analysis import save_sentiment
from src.lda_modeling import fit_lda, display_topics

STAGES = {
    "clean", 
    "cluster", 
    "topics", 
    "viz", 
    "sentiment", 
    "lda"
}

def run_optimized(slug: str, stage: str, sample_size: int = 5000, n_jobs: int = -1, 
                 cache_dir: Path = None, k: int = None):
    """
    Run the optimized pipeline.
    
    Args:
        slug: Dataset identifier
        stage: Pipeline stage to run
        sample_size: Sample size for k selection
        n_jobs: Number of parallel jobs
        cache_dir: Directory for caching results
        k: Number of clusters (if known)
    """
    print(f"🚀 Starting OPTIMIZED pipeline for dataset: {slug}")
    print(f"📋 Stage: {stage}")
    print(f"⚡ Using {n_jobs if n_jobs > 0 else mp.cpu_count()} parallel jobs")
    
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
        
        # Find optimal k if not provided
        if k is None:
            print("🎲 Finding optimal k using sampling...")
            k = sample_based_k_selection(
                X, 
                sample_size=sample_size,
                k_range=(2, 12),
                random_state=42
            )
            print(f"🎯 Optimal k: {k}")
        else:
            print(f"🎯 Using provided k: {k}")
        
        # Perform clustering with optimized method
        print("🔀 Performing clustering...")
        from sklearn.cluster import MiniBatchKMeans
        km = MiniBatchKMeans(
            n_clusters=k, 
            batch_size=1000, 
            random_state=42,
            n_init=3
        )
        df["cluster"] = km.fit_predict(X)
        
        # Save model
        model_path = config.MODEL_DIR / f"{slug}_kmeans_k{k}.pkl"
        import joblib
        joblib.dump(km, model_path)
        
        out = config.DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        df.to_parquet(out, index=False)
        print(f"✅ Clustering done (k={k}), saved to {out}")
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

def run_chunked_pipeline(slug: str, chunk_size: int = 10000, n_jobs: int = -1):
    """
    Run the pipeline on chunked data for very large datasets.
    
    Args:
        slug: Dataset identifier
        chunk_size: Size of each chunk
        n_jobs: Number of parallel jobs
    """
    print(f"🔀 Starting CHUNKED pipeline for dataset: {slug}")
    print(f"📦 Chunk size: {chunk_size:,}")
    print(f"⚡ Parallel jobs: {n_jobs if n_jobs > 0 else mp.cpu_count()}")
    
    # Step 1: Split data into chunks
    print("✂️  Splitting data into chunks...")
    from scripts.split_data import split_csv_file
    chunk_dir = config.DATA_DIR / "chunks" / slug
    split_csv_file(
        input_file=config.DATASETS[slug],
        output_dir=chunk_dir,
        chunk_size=chunk_size
    )
    
    # Step 2: Process chunks in parallel
    print("🚀 Processing chunks in parallel...")
    from scripts.process_chunks_parallel import process_chunks_parallel
    output_dir = config.DATA_DIR / "processed_chunks" / slug
    processed_chunks = process_chunks_parallel(
        chunk_dir=chunk_dir,
        output_dir=output_dir,
        k=None,  # Find optimal k for each chunk
        n_jobs=n_jobs,
        sample_size=5000
    )
    
    # Step 3: Combine results
    print("🔗 Combining processed chunks...")
    from scripts.process_chunks_parallel import combine_chunk_results
    final_output = config.DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
    combine_chunk_results(processed_chunks, final_output)
    
    print(f"🎉 Chunked pipeline completed! Results saved to {final_output}")

def main():
    p = ArgumentParser()
    p.add_argument(
        "--set", choices=config.DATASETS.keys(), required=True,
        help="Which dataset to process (high_rating | most_commented)"
    )
    p.add_argument(
        "--stage", choices=STAGES, default="clean",
        help="Pipeline stage to run"
    )
    p.add_argument(
        "--optimized", action="store_true",
        help="Use optimized pipeline with sampling and parallel processing"
    )
    p.add_argument(
        "--chunked", action="store_true",
        help="Use chunked pipeline for very large datasets"
    )
    p.add_argument(
        "--sample-size", type=int, default=5000,
        help="Sample size for k selection (optimized mode)"
    )
    p.add_argument(
        "--n-jobs", type=int, default=-1,
        help="Number of parallel jobs (-1 for all CPUs)"
    )
    p.add_argument(
        "--k", type=int,
        help="Number of clusters (if known, skips k selection)"
    )
    p.add_argument(
        "--chunk-size", type=int, default=10000,
        help="Chunk size for chunked pipeline"
    )
    p.add_argument(
        "--cache-dir",
        help="Directory for caching results"
    )
    
    args = p.parse_args()
    
    # Set cache directory
    cache_dir = Path(args.cache_dir) if args.cache_dir else config.DATA_DIR / "cache"
    
    # Run appropriate pipeline
    if args.chunked:
        run_chunked_pipeline(
            slug=args.set,
            chunk_size=args.chunk_size,
            n_jobs=args.n_jobs
        )
    elif args.optimized:
        run_optimized(
            slug=args.set,
            stage=args.stage,
            sample_size=args.sample_size,
            n_jobs=args.n_jobs,
            cache_dir=cache_dir,
            k=args.k
        )
    else:
        # Original pipeline (for comparison)
        from main import run
        run(args.set, args.stage)

if __name__ == "__main__":
    main() 