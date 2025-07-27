#!/usr/bin/env python3
"""
Test clustering on a smaller sample to verify the ない fix works.
"""

import pandas as pd
from pathlib import Path
from src import config
from src.data_collection import load_raw
from src.text_cleaning import cleanse_dataframe
from src.vectorize import build_tfidf
from src.cluster_eval import best_k_silhouette
from src.clustering import fit_kmeans

def test_clustering():
    print("🧪 Testing clustering on a sample...")
    
    # Load raw data
    df = load_raw(config.DATASETS["high_rating"])
    
    # Take a smaller sample (10k records)
    sample_size = 10000
    df_sample = df.sample(n=sample_size, random_state=42)
    print(f"📊 Using sample of {len(df_sample):,} records")
    
    # Clean the sample
    df_sample = cleanse_dataframe(df_sample, text_col="comment")
    
    # Check if ない is still appearing frequently
    all_text = " ".join(df_sample["clean_joined"].dropna())
    words = all_text.split()
    from collections import Counter
    word_counts = Counter(words)
    
    print("\n🔍 Top 20 most frequent words:")
    for word, count in word_counts.most_common(20):
        print(f"  {word}: {count}")
    
    # Build TF-IDF with smaller parameters
    print("\n🔄 Building TF-IDF vectors (sample)...")
    X, vec = build_tfidf(df_sample, max_features=5000, min_df=10, max_df=0.8)
    
    # Test silhouette scores
    print("\n🔄 Testing silhouette scores...")
    best_k, scores = best_k_silhouette(X, k_min=2, k_max=5)  # Test fewer k values
    
    print(f"\n✅ Test completed! Best k: {best_k}")
    return best_k, scores

if __name__ == "__main__":
    test_clustering() 