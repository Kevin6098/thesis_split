#!/usr/bin/env python3
"""
Simple clustering with fixed k value to skip silhouette evaluation.
"""

import pandas as pd
from pathlib import Path
from src import config
from src.data_collection import load_raw
from src.text_cleaning import cleanse_dataframe
from src.vectorize import build_tfidf
from src.clustering import fit_kmeans

def simple_cluster(k=3):
    print(f"🚀 Simple clustering with k={k}")
    
    # Load raw data
    print("📥 Loading raw data...")
    df = load_raw(config.DATASETS["high_rating"])
    print(f"✅ Loaded {len(df):,} records")
    
    # Clean the data
    df = cleanse_dataframe(df, text_col="comment")
    
    # Build TF-IDF vectors
    print("🔄 Building TF-IDF vectors...")
    X, vec = build_tfidf(df, max_features=10_000, min_df=20, max_df=0.85)
    
    # Fit K-means with fixed k
    print(f"🔄 Fitting K-means with k={k}...")
    model_path = config.MODEL_DIR / f"high_rating_kmeans_k{k}.pkl"
    km = fit_kmeans(X, k, model_path)
    
    # Add cluster labels to dataframe
    df["cluster"] = km.labels_
    
    # Save results
    out = config.DATA_DIR / "processed" / f"high_rating_with_clusters.parquet"
    df.to_parquet(out, index=False)
    print(f"✅ Clustering completed! Results saved to {out}")
    
    # Show cluster distribution
    print("\n📊 Cluster distribution:")
    cluster_counts = df["cluster"].value_counts().sort_index()
    for cluster, count in cluster_counts.items():
        print(f"  Cluster {cluster}: {count:,} records ({count/len(df)*100:.1f}%)")
    
    return df, km

if __name__ == "__main__":
    simple_cluster(k=3) 