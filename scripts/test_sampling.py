#!/usr/bin/env python
"""
Test script to demonstrate sampling-based silhouette score calculation.
This shows the performance difference between original and sampling methods.
"""

import time
import pandas as pd
import numpy as np
from pathlib import Path
import argparse

def test_sampling_methods(input_file: Path, sample_size: int = 100000):
    """
    Test different sampling methods for silhouette score calculation.
    
    Args:
        input_file: Path to input data file
        sample_size: Sample size for testing (default: 100k)
    """
    print(f"🧪 Testing sampling methods on {input_file}")
    
    # Load data
    df = pd.read_parquet(input_file)
    print(f"📥 Loaded {len(df):,} records")
    
    # Build TF-IDF
    from src.vectorize import build_tfidf
    X, _ = build_tfidf(df)
    print(f"📊 TF-IDF shape: {X.shape}")
    
    # Test 1: Original method (no sampling)
    print("\n" + "="*50)
    print("🧪 TEST 1: Original Method (No Sampling)")
    print("="*50)
    
    start_time = time.time()
    
    from src.cluster_eval import best_k_silhouette
    best_k_orig, scores_orig = best_k_silhouette(
        X, 
        k_min=2, 
        k_max=6,  # Reduced range for testing
        use_sampling=False
    )
    
    elapsed_orig = time.time() - start_time
    print(f"⏱️  Original method: {elapsed_orig:.2f}s")
    print(f"🎯 Best k: {best_k_orig}")
    
    # Test 2: Sampling method
    print("\n" + "="*50)
    print("🎲 TEST 2: Sampling Method")
    print("="*50)
    
    start_time = time.time()
    
    best_k_sample, scores_sample = best_k_silhouette(
        X, 
        k_min=2, 
        k_max=6,  # Reduced range for testing
        use_sampling=True,
        sample_size=sample_size
    )
    
    elapsed_sample = time.time() - start_time
    print(f"⏱️  Sampling method: {elapsed_sample:.2f}s")
    print(f"🎯 Best k: {best_k_sample}")
    
    # Test 3: Fast sampling method
    print("\n" + "="*50)
    print("🚀 TEST 3: Fast Sampling Method")
    print("="*50)
    
    start_time = time.time()
    
    from src.cluster_eval import fast_best_k_silhouette
    best_k_fast, scores_fast = fast_best_k_silhouette(
        X, 
        k_min=2, 
        k_max=6,  # Reduced range for testing
        sample_size=sample_size
    )
    
    elapsed_fast = time.time() - start_time
    print(f"⏱️  Fast sampling method: {elapsed_fast:.2f}s")
    print(f"🎯 Best k: {best_k_fast}")
    
    # Results comparison
    print("\n" + "="*50)
    print("📊 PERFORMANCE COMPARISON")
    print("="*50)
    
    speedup_sample = elapsed_orig / elapsed_sample if elapsed_sample > 0 else float('inf')
    speedup_fast = elapsed_orig / elapsed_fast if elapsed_fast > 0 else float('inf')
    
    print(f"Original method:     {elapsed_orig:.2f}s")
    print(f"Sampling method:     {elapsed_sample:.2f}s ({speedup_sample:.1f}x faster)")
    print(f"Fast sampling:       {elapsed_fast:.2f}s ({speedup_fast:.1f}x faster)")
    
    print(f"\nBest k values:")
    print(f"  Original:  {best_k_orig}")
    print(f"  Sampling:  {best_k_sample}")
    print(f"  Fast:      {best_k_fast}")
    
    # Compare scores for same k values
    print(f"\nSilhouette scores comparison:")
    for k in sorted(set(scores_orig.keys()) & set(scores_sample.keys()) & set(scores_fast.keys())):
        print(f"  k={k}: Original={scores_orig[k]:.4f}, Sampling={scores_sample[k]:.4f}, Fast={scores_fast[k]:.4f}")
    
    return {
        'original_time': elapsed_orig,
        'sampling_time': elapsed_sample,
        'fast_time': elapsed_fast,
        'original_k': best_k_orig,
        'sampling_k': best_k_sample,
        'fast_k': best_k_fast
    }

def main():
    parser = argparse.ArgumentParser(description="Test sampling-based silhouette score calculation")
    parser.add_argument("--input", required=True, help="Input data file (parquet)")
    parser.add_argument("--sample-size", type=int, default=100000, help="Sample size for testing (default: 100000)")
    
    args = parser.parse_args()
    
    input_file = Path(args.input)
    if not input_file.exists():
        print(f"❌ Input file not found: {input_file}")
        return
    
    # Run tests
    results = test_sampling_methods(input_file, args.sample_size)
    
    print(f"\n💡 Recommendations:")
    print(f"  • Use --sample-size 100000 for good balance of speed and accuracy")
    print(f"  • Use --parallel flag for even faster processing")
    print(f"  • Use --no-sampling only for small datasets or when accuracy is critical")

if __name__ == "__main__":
    main() 