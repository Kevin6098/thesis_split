#!/usr/bin/env python
"""
Optimized clustering with parallel processing, sampling, and caching.
This module provides faster alternatives to the original clustering functions.
"""

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans, MiniBatchKMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score
from sklearn.metrics.pairwise import pairwise_distances
from sklearn.utils import resample
import joblib
from pathlib import Path
import time
from typing import Dict, Tuple, List, Optional
import multiprocessing as mp
from functools import partial
import warnings

def fast_silhouette_score(X, labels, sample_size: int = 10000):
    """
    Calculate approximate silhouette score using sampling.
    Much faster than full silhouette calculation for large datasets.
    
    Args:
        X: Feature matrix
        labels: Cluster labels
        sample_size: Number of samples to use for approximation
    
    Returns:
        Approximate silhouette score
    """
    if len(X) <= sample_size:
        return silhouette_score(X, labels)
    
    # Sample data for faster computation
    indices = np.random.choice(len(X), sample_size, replace=False)
    X_sample = X[indices]
    labels_sample = labels[indices]
    
    return silhouette_score(X_sample, labels_sample)

def parallel_k_evaluation(X, k_values: List[int], n_jobs: int = -1, 
                        sample_size: int = 10000, random_state: int = 42):
    """
    Evaluate multiple k values in parallel using sampling.
    
    Args:
        X: Feature matrix
        k_values: List of k values to test
        n_jobs: Number of parallel jobs (-1 for all CPUs)
        sample_size: Sample size for silhouette calculation
        random_state: Random seed
    
    Returns:
        Dictionary of k -> score mappings
    """
    print(f"🔄 Evaluating {len(k_values)} k values in parallel...")
    
    def evaluate_single_k(k, X_data, sample_sz, rs):
        """Evaluate a single k value."""
        np.random.seed(rs)
        
        # Use MiniBatchKMeans for faster clustering
        km = MiniBatchKMeans(
            n_clusters=k, 
            batch_size=1000,
            random_state=rs,
            n_init=3  # Reduced from default
        )
        
        # Fit on sample for speed
        if len(X_data) > sample_sz:
            sample_indices = np.random.choice(len(X_data), sample_sz, replace=False)
            X_sample = X_data[sample_indices]
        else:
            X_sample = X_data
        
        labels = km.fit_predict(X_sample)
        
        # Calculate silhouette on sample
        sil_score = silhouette_score(X_sample, labels)
        
        # Also calculate Calinski-Harabasz for comparison
        ch_score = calinski_harabasz_score(X_sample, labels)
        
        return k, sil_score, ch_score
    
    # Prepare function for parallel processing
    eval_func = partial(evaluate_single_k, X_data=X, sample_sz=sample_size, rs=random_state)
    
    # Run in parallel
    with mp.Pool(processes=n_jobs if n_jobs > 0 else mp.cpu_count()) as pool:
        results = pool.map(eval_func, k_values)
    
    # Organize results
    scores = {}
    for k, sil_score, ch_score in results:
        scores[k] = {
            'silhouette': sil_score,
            'calinski_harabasz': ch_score
        }
        print(f"  k={k:2d} → silhouette={sil_score:.4f}, ch={ch_score:.2f}")
    
    return scores

def optimized_best_k_silhouette(X, k_min: int = 2, k_max: int = 10, 
                               sample_size: int = 10000, n_jobs: int = -1,
                               random_state: int = 42, cache_dir: Optional[Path] = None):
    """
    Optimized version of best_k_silhouette with parallel processing and caching.
    
    Args:
        X: Feature matrix
        k_min: Minimum k value
        k_max: Maximum k value
        sample_size: Sample size for silhouette calculation
        n_jobs: Number of parallel jobs
        random_state: Random seed
        cache_dir: Directory to cache results
    
    Returns:
        Best k value and all scores
    """
    print("🚀 Optimized k evaluation with parallel processing...")
    
    k_values = list(range(k_min, k_max + 1))
    
    # Check cache first
    if cache_dir:
        cache_file = cache_dir / f"k_evaluation_cache_{len(X)}_{k_min}_{k_max}.joblib"
        if cache_file.exists():
            print(f"📁 Loading cached results from {cache_file}")
            return joblib.load(cache_file)
    
    # Run parallel evaluation
    start_time = time.time()
    scores = parallel_k_evaluation(X, k_values, n_jobs, sample_size, random_state)
    elapsed = time.time() - start_time
    
    print(f"⏱️  Evaluation completed in {elapsed:.2f}s")
    
    # Find best k based on silhouette score
    best_k = max(scores.keys(), key=lambda k: scores[k]['silhouette'])
    best_score = scores[best_k]['silhouette']
    
    print(f"✅ Best k: {best_k} (silhouette={best_score:.4f})")
    
    # Cache results
    if cache_dir:
        cache_dir.mkdir(parents=True, exist_ok=True)
        joblib.dump((best_k, scores), cache_file)
        print(f"💾 Cached results to {cache_file}")
    
    return best_k, scores

def chunked_clustering(X, chunk_size: int = 10000, k: int = 8, 
                      random_state: int = 42, n_jobs: int = -1):
    """
    Perform clustering on data in chunks to reduce memory usage.
    
    Args:
        X: Feature matrix
        chunk_size: Size of each chunk
        k: Number of clusters
        random_state: Random seed
        n_jobs: Number of parallel jobs
    
    Returns:
        Cluster labels for all data
    """
    print(f"🔀 Performing chunked clustering (k={k}, chunk_size={chunk_size:,})...")
    
    n_samples = X.shape[0]
    labels = np.zeros(n_samples, dtype=int)
    
    # Process in chunks
    for i in range(0, n_samples, chunk_size):
        end_idx = min(i + chunk_size, n_samples)
        chunk = X[i:end_idx]
        
        print(f"  📦 Processing chunk {i//chunk_size + 1}/{(n_samples + chunk_size - 1)//chunk_size}")
        
        # Use MiniBatchKMeans for faster processing
        km = MiniBatchKMeans(
            n_clusters=k,
            batch_size=min(1000, len(chunk)),
            random_state=random_state,
            n_init=3
        )
        
        chunk_labels = km.fit_predict(chunk)
        labels[i:end_idx] = chunk_labels
    
    print(f"✅ Chunked clustering completed")
    return labels

def sample_based_k_selection(X, sample_size: int = 5000, k_range: Tuple[int, int] = (2, 12),
                           random_state: int = 42):
    """
    Use sampling to quickly find optimal k, then apply to full dataset.
    
    Args:
        X: Feature matrix
        sample_size: Size of sample for k selection
        k_range: Range of k values to test
        random_state: Random seed
    
    Returns:
        Optimal k value
    """
    print(f"🎲 Using sampling for k selection (sample_size={sample_size:,})...")
    
    # Take a sample
    if len(X) > sample_size:
        sample_indices = np.random.choice(len(X), sample_size, replace=False, random_state=random_state)
        X_sample = X[sample_indices]
    else:
        X_sample = X
    
    print(f"📊 Sample shape: {X_sample.shape}")
    
    # Find optimal k on sample
    best_k, _ = optimized_best_k_silhouette(
        X_sample, 
        k_min=k_range[0], 
        k_max=k_range[1],
        sample_size=min(2000, sample_size//2),  # Smaller sample for silhouette
        random_state=random_state
    )
    
    print(f"🎯 Optimal k from sample: {best_k}")
    return best_k

def process_chunk_parallel(chunk_file: Path, output_dir: Path, k: int, 
                         random_state: int = 42):
    """
    Process a single chunk file (for parallel processing).
    
    Args:
        chunk_file: Path to chunk CSV file
        output_dir: Output directory
        k: Number of clusters
        random_state: Random seed
    
    Returns:
        Path to processed chunk file
    """
    print(f"🔄 Processing {chunk_file.name}...")
    
    # Load chunk
    df = pd.read_csv(chunk_file)
    
    # Clean text (assuming clean_joined column exists)
    if 'clean_joined' not in df.columns:
        from src.text_cleaning import cleanse_dataframe
        df = cleanse_dataframe(df, text_col="comment")
    
    # Build TF-IDF
    from src.vectorize import build_tfidf
    X, _ = build_tfidf(df)
    
    # Cluster
    km = MiniBatchKMeans(n_clusters=k, batch_size=1000, random_state=random_state)
    df['cluster'] = km.fit_predict(X)
    
    # Save processed chunk
    output_file = output_dir / f"{chunk_file.stem}_processed.parquet"
    df.to_parquet(output_file, index=False)
    
    print(f"✅ Processed {len(df):,} records → {output_file.name}")
    return output_file

def main():
    """Example usage of optimized clustering."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Optimized clustering with parallel processing")
    parser.add_argument("--input", required=True, help="Input data file")
    parser.add_argument("--output", required=True, help="Output file")
    parser.add_argument("--k", type=int, help="Number of clusters (if known)")
    parser.add_argument("--k-min", type=int, default=2, help="Minimum k for evaluation")
    parser.add_argument("--k-max", type=int, default=10, help="Maximum k for evaluation")
    parser.add_argument("--sample-size", type=int, default=5000, help="Sample size for k selection")
    parser.add_argument("--chunk-size", type=int, default=10000, help="Chunk size for processing")
    parser.add_argument("--n-jobs", type=int, default=-1, help="Number of parallel jobs")
    parser.add_argument("--cache-dir", help="Directory for caching results")
    
    args = parser.parse_args()
    
    # Load data
    print(f"📥 Loading {args.input}...")
    df = pd.read_parquet(args.input)
    print(f"✅ Loaded {len(df):,} records")
    
    # Build TF-IDF
    from src.vectorize import build_tfidf
    X, _ = build_tfidf(df)
    
    # Find optimal k if not provided
    if args.k is None:
        print("🔍 Finding optimal k...")
        args.k = sample_based_k_selection(
            X, 
            sample_size=args.sample_size,
            k_range=(args.k_min, args.k_max)
        )
    
    # Perform clustering
    print(f"🎯 Clustering with k={args.k}...")
    km = MiniBatchKMeans(n_clusters=args.k, batch_size=1000, random_state=42)
    df['cluster'] = km.fit_predict(X)
    
    # Save results
    df.to_parquet(args.output, index=False)
    print(f"✅ Results saved to {args.output}")

if __name__ == "__main__":
    main() 