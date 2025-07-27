#!/usr/bin/env python
"""
Split large CSV files into smaller chunks for faster processing.
This allows parallel processing of data chunks.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import argparse
from typing import List

def split_csv_file(
    input_file: Path,
    output_dir: Path,
    chunk_size: int = 10000,
    random_sample: bool = False,
    sample_size: int = None
):
    """
    Split a large CSV file into smaller chunks.
    
    Args:
        input_file: Path to the input CSV file
        output_dir: Directory to save chunk files
        chunk_size: Number of rows per chunk
        random_sample: Whether to take a random sample first
        sample_size: Size of random sample (if random_sample=True)
    """
    print(f"📥 Loading {input_file}...")
    df = pd.read_csv(input_file)
    print(f"✅ Loaded {len(df):,} records")
    
    if random_sample and sample_size:
        print(f"🎲 Taking random sample of {sample_size:,} records...")
        df = df.sample(n=min(sample_size, len(df)), random_state=42)
        print(f"✅ Sampled {len(df):,} records")
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Split into chunks
    n_chunks = (len(df) + chunk_size - 1) // chunk_size
    print(f"✂️  Splitting into {n_chunks} chunks of ~{chunk_size:,} records each...")
    
    for i in range(n_chunks):
        start_idx = i * chunk_size
        end_idx = min((i + 1) * chunk_size, len(df))
        chunk = df.iloc[start_idx:end_idx]
        
        # Save chunk
        chunk_file = output_dir / f"chunk_{i:03d}.csv"
        chunk.to_csv(chunk_file, index=False)
        print(f"  ✅ Saved chunk {i+1}/{n_chunks}: {len(chunk):,} records → {chunk_file}")
    
    print(f"🎉 All chunks saved to {output_dir}")

def combine_chunk_results(chunk_dir: Path, output_file: Path):
    """
    Combine results from processed chunks back into a single file.
    
    Args:
        chunk_dir: Directory containing processed chunk files
        output_file: Path for the combined output file
    """
    print(f"🔗 Combining results from {chunk_dir}...")
    
    # Find all processed chunk files
    chunk_files = list(chunk_dir.glob("*_processed.parquet"))
    if not chunk_files:
        print("❌ No processed chunk files found!")
        return
    
    print(f"📁 Found {len(chunk_files)} processed chunks...")
    
    # Load and combine chunks
    dfs = []
    for chunk_file in sorted(chunk_files):
        df = pd.read_parquet(chunk_file)
        dfs.append(df)
        print(f"  ✅ Loaded {len(df):,} records from {chunk_file.name}")
    
    # Combine all chunks
    combined_df = pd.concat(dfs, ignore_index=True)
    combined_df.to_parquet(output_file, index=False)
    print(f"🎉 Combined {len(combined_df):,} total records → {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Split CSV files into chunks for faster processing")
    parser.add_argument("--input", required=True, help="Input CSV file path")
    parser.add_argument("--output-dir", required=True, help="Output directory for chunks")
    parser.add_argument("--chunk-size", type=int, default=10000, help="Records per chunk")
    parser.add_argument("--random-sample", action="store_true", help="Take random sample first")
    parser.add_argument("--sample-size", type=int, help="Size of random sample")
    parser.add_argument("--combine", action="store_true", help="Combine processed chunks")
    
    args = parser.parse_args()
    
    input_file = Path(args.input)
    output_dir = Path(args.output_dir)
    
    if args.combine:
        combine_chunk_results(output_dir, output_dir / "combined_results.parquet")
    else:
        split_csv_file(
            input_file=input_file,
            output_dir=output_dir,
            chunk_size=args.chunk_size,
            random_sample=args.random_sample,
            sample_size=args.sample_size
        )

if __name__ == "__main__":
    main() 