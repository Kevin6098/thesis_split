#!/usr/bin/env python
"""
Performance comparison between original and optimized clustering methods.
This script helps you understand the speed improvements.
"""

import time
import pandas as pd
import numpy as np
from pathlib import Path
import argparse
from typing import Dict, Tuple

def compare_methods(input_file: Path, sample_size: int = 10000):
    """
    Compare performance of original vs optimized methods.
    
    Args:
        input_file: Path to input data file
        sample_size: Sample size for testing
    """
    print(f"🔍 Comparing clustering methods on {input_file}")
    
    # Load data
    df = pd.read_parquet(input_file)
    print(f"📥 Loaded {len(df):,} records")
    
    # Take a sample for testing
    if len(df) > sample_size:
        df_sample = df.sample(n=sample_size, random_state=42)
        print(f"🎲 Using sample of {len(df_sample):,} records for testing")
    else:
        df_sample = df
        print(f"📊 Using full dataset ({len(df_sample):,} records)")
    
    # Build TF-IDF
    from src.vectorize import build_tfidf
    X, _ = build_tfidf(df_sample)
    print(f"📊 TF-IDF shape: {X.shape}")
    
    # Test 1: Original method
    print("\n" + "="*50)
    print("🧪 TEST 1: Original Method")
    print("="*50)
    
    start_time = time.time()
    
    from src.cluster_eval import best_k_silhouette
    best_k_orig, scores_orig = best_k_silhouette(X, k_min=2, k_max=8)
    
    elapsed_orig = time.time() - start_time
    print(f"⏱️  Original method: {elapsed_orig:.2f}s")
    print(f"🎯 Best k: {best_k_orig}")
    
    # Test 2: Optimized method
    print("\n" + "="*50)
    print("🚀 TEST 2: Optimized Method")
    print("="*50)
    
    start_time = time.time()
    
    from src.optimized_clustering import optimized_best_k_silhouette
    best_k_opt, scores_opt = optimized_best_k_silhouette(
        X, 
        k_min=2, 
        k_max=8,
        sample_size=2000,  # Smaller sample for silhouette
        n_jobs=-1  # Use all CPUs
    )
    
    elapsed_opt = time.time() - start_time
    print(f"⏱️  Optimized method: {elapsed_opt:.2f}s")
    print(f"🎯 Best k: {best_k_opt}")
    
    # Test 3: Sampling-based k selection
    print("\n" + "="*50)
    print("🎲 TEST 3: Sampling-based k Selection")
    print("="*50)
    
    start_time = time.time()
    
    from src.optimized_clustering import sample_based_k_selection
    best_k_sample = sample_based_k_selection(
        X,
        sample_size=3000,
        k_range=(2, 8),
        random_state=42
    )
    
    elapsed_sample = time.time() - start_time
    print(f"⏱️  Sampling method: {elapsed_sample:.2f}s")
    print(f"🎯 Best k: {best_k_sample}")
    
    # Results comparison
    print("\n" + "="*50)
    print("📊 PERFORMANCE COMPARISON")
    print("="*50)
    
    speedup_opt = elapsed_orig / elapsed_opt if elapsed_opt > 0 else float('inf')
    speedup_sample = elapsed_orig / elapsed_sample if elapsed_sample > 0 else float('inf')
    
    print(f"Original method:     {elapsed_orig:.2f}s")
    print(f"Optimized method:    {elapsed_opt:.2f}s ({speedup_opt:.1f}x faster)")
    print(f"Sampling method:     {elapsed_sample:.2f}s ({speedup_sample:.1f}x faster)")
    
    print(f"\nBest k values:")
    print(f"  Original:  {best_k_orig}")
    print(f"  Optimized: {best_k_opt}")
    print(f"  Sampling:  {best_k_sample}")
    
    # Accuracy comparison (if k values are different)
    if best_k_orig != best_k_opt or best_k_orig != best_k_sample:
        print(f"\n⚠️  Note: Different k values found by different methods")
        print(f"   This is normal due to sampling and different algorithms")
    
    return {
        'original_time': elapsed_orig,
        'optimized_time': elapsed_opt,
        'sampling_time': elapsed_sample,
        'original_k': best_k_orig,
        'optimized_k': best_k_opt,
        'sampling_k': best_k_sample
    }

def estimate_full_dataset_time(results: Dict, full_dataset_size: int, test_sample_size: int):
    """
    Estimate time for full dataset based on test results.
    
    Args:
        results: Results from compare_methods
        full_dataset_size: Size of full dataset
        test_sample_size: Size of test sample
    """
    print(f"\n" + "="*50)
    print("📈 ESTIMATED FULL DATASET TIMES")
    print("="*50)
    
    # Scale factor
    scale_factor = full_dataset_size / test_sample_size
    
    # Estimate times (assuming linear scaling for clustering)
    orig_est = results['original_time'] * scale_factor
    opt_est = results['optimized_time'] * scale_factor
    sample_est = results['sampling_time'] * scale_factor
    
    print(f"Full dataset size: {full_dataset_size:,} records")
    print(f"Test sample size:  {test_sample_size:,} records")
    print(f"Scale factor:      {scale_factor:.1f}x")
    
    print(f"\nEstimated times for full dataset:")
    print(f"  Original method:     {orig_est/60:.1f} minutes ({orig_est/3600:.1f} hours)")
    print(f"  Optimized method:    {opt_est/60:.1f} minutes ({opt_est/3600:.1f} hours)")
    print(f"  Sampling method:     {sample_est/60:.1f} minutes ({sample_est/3600:.1f} hours)")
    
    # Savings
    if orig_est > 0:
        savings_opt = (orig_est - opt_est) / orig_est * 100
        savings_sample = (orig_est - sample_est) / orig_est * 100
        print(f"\nTime savings:")
        print(f"  Optimized: {savings_opt:.1f}% faster")
        print(f"  Sampling:  {savings_sample:.1f}% faster")

def main():
    parser = argparse.ArgumentParser(description="Compare clustering method performance")
    parser.add_argument("--input", required=True, help="Input data file (parquet)")
    parser.add_argument("--sample-size", type=int, default=10000, help="Sample size for testing")
    parser.add_argument("--full-size", type=int, help="Full dataset size for estimation")
    
    args = parser.parse_args()
    
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    # Run comparison
    results = compare_methods(input_file, args.sample_size)
    
    # Estimate full dataset times if full size provided
    if args.full_size:
        estimate_full_dataset_time(results, args.full_size, args.sample_size)
    
    print(f"\n💡 Recommendations:")
    print(f"  • Use --optimized flag for faster processing")
    print(f"  • Use --chunked flag for very large datasets")
    print(f"  • Use --k <value> if you know the optimal k")
    print(f"  • Use --sample-size <value> to adjust sampling")

if __name__ == "__main__":
    main() 