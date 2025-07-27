#!/usr/bin/env python
"""
Process data chunks in parallel for maximum speed.
This script takes chunked CSV files and processes them in parallel.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import argparse
import multiprocessing as mp
from functools import partial
import time
from typing import List, Tuple
import warnings

def process_single_chunk(chunk_file: Path, output_dir: Path, k: int, 
                        sample_size: int = 5000, random_state: int = 42):
    """
    Process a single chunk file.
    
    Args:
        chunk_file: Path to chunk CSV file
        output_dir: Output directory
        k: Number of clusters
        sample_size: Sample size for k selection (if k is None)
        random_state: Random seed
    
    Returns:
        Path to processed chunk file
    """
    try:
        print(f"🔄 Processing {chunk_file.name}...")
        
        # Load chunk
        df = pd.read_csv(chunk_file)
        print(f"  📥 Loaded {len(df):,} records")
        
        # Clean text if needed
        if 'clean_joined' not in df.columns:
            from src.text_cleaning import cleanse_dataframe
            df = cleanse_dataframe(df, text_col="comment")
            print(f"  🧹 Text cleaned")
        
        # Build TF-IDF
        from src.vectorize import build_tfidf
        X, _ = build_tfidf(df)
        print(f"  📊 TF-IDF built: {X.shape}")
        
        # Find optimal k if not provided
        if k is None:
            print(f"  🔍 Finding optimal k on sample...")
            from src.optimized_clustering import sample_based_k_selection
            k = sample_based_k_selection(X, sample_size=sample_size, random_state=random_state)
            print(f"  🎯 Optimal k: {k}")
        
        # Perform clustering
        from sklearn.cluster import MiniBatchKMeans
        km = MiniBatchKMeans(n_clusters=k, batch_size=1000, random_state=random_state)
        df['cluster'] = km.fit_predict(X)
        print(f"  🎯 Clustering completed (k={k})")
        
        # Save processed chunk
        output_file = output_dir / f"{chunk_file.stem}_processed.parquet"
        df.to_parquet(output_file, index=False)
        
        print(f"  ✅ Saved {len(df):,} records → {output_file.name}")
        return output_file
        
    except Exception as e:
        print(f"  ❌ Error processing {chunk_file.name}: {e}")
        return None

def process_chunks_parallel(chunk_dir: Path, output_dir: Path, k: int = None,
                          n_jobs: int = -1, sample_size: int = 5000, 
                          random_state: int = 42):
    """
    Process all chunks in parallel.
    
    Args:
        chunk_dir: Directory containing chunk files
        output_dir: Output directory for processed chunks
        k: Number of clusters (if None, will find optimal k for each chunk)
        n_jobs: Number of parallel jobs
        sample_size: Sample size for k selection
        random_state: Random seed
    """
    # Find all chunk files
    chunk_files = list(chunk_dir.glob("chunk_*.csv"))
    if not chunk_files:
        print(f"❌ No chunk files found in {chunk_dir}")
        return
    
    print(f"📁 Found {len(chunk_files)} chunk files")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Prepare function for parallel processing
    process_func = partial(
        process_single_chunk,
        output_dir=output_dir,
        k=k,
        sample_size=sample_size,
        random_state=random_state
    )
    
    # Set number of jobs
    if n_jobs <= 0:
        n_jobs = mp.cpu_count()
    
    print(f"🚀 Processing {len(chunk_files)} chunks with {n_jobs} parallel jobs...")
    start_time = time.time()
    
    # Process in parallel
    with mp.Pool(processes=n_jobs) as pool:
        results = pool.map(process_func, chunk_files)
    
    # Filter out failed chunks
    successful_results = [r for r in results if r is not None]
    
    elapsed = time.time() - start_time
    print(f"⏱️  Processing completed in {elapsed:.2f}s")
    print(f"✅ Successfully processed {len(successful_results)}/{len(chunk_files)} chunks")
    
    return successful_results

def combine_chunk_results(processed_chunks: List[Path], output_file: Path):
    """
    Combine all processed chunks into a single file.
    
    Args:
        processed_chunks: List of processed chunk file paths
        output_file: Path for combined output file
    """
    print(f"🔗 Combining {len(processed_chunks)} processed chunks...")
    
    dfs = []
    total_records = 0
    
    for chunk_file in sorted(processed_chunks):
        df = pd.read_parquet(chunk_file)
        dfs.append(df)
        total_records += len(df)
        print(f"  ✅ Loaded {len(df):,} records from {chunk_file.name}")
    
    # Combine all chunks
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_parquet(output_file, index=False)
    
    print(f"🎉 Combined {total_records:,} total records → {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Process data chunks in parallel")
    parser.add_argument("--chunk-dir", required=True, help="Directory containing chunk files")
    parser.add_argument("--output-dir", required=True, help="Output directory for processed chunks")
    parser.add_argument("--k", type=int, help="Number of clusters (if None, will find optimal k)")
    parser.add_argument("--n-jobs", type=int, default=-1, help="Number of parallel jobs")
    parser.add_argument("--sample-size", type=int, default=5000, help="Sample size for k selection")
    parser.add_argument("--combine", action="store_true", help="Combine processed chunks")
    parser.add_argument("--final-output", help="Final output file (if combining)")
    
    args = parser.parse_args()
    
    chunk_dir = Path(args.chunk_dir)
    output_dir = Path(args.output_dir)
    
    # Process chunks in parallel
    processed_chunks = process_chunks_parallel(
        chunk_dir=chunk_dir,
        output_dir=output_dir,
        k=args.k,
        n_jobs=args.n_jobs,
        sample_size=args.sample_size
    )
    
    # Combine results if requested
    if args.combine and processed_chunks:
        if args.final_output:
            final_output = Path(args.final_output)
        else:
            final_output = output_dir / "combined_results.parquet"
        
        combine_chunk_results(processed_chunks, final_output)

if __name__ == "__main__":
    main() 