#!/usr/bin/env python3
"""
Data Preparation Script
Cleans, tokenizes, and vectorizes text data for clustering.
Exports TF-IDF vectors to CSV for use in K-means clustering.
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import time

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from text_cleaning import cleanse_dataframe
from vectorize import build_tfidf
from config import DATA_DIR

def prepare_data(
    input_file: str,
    text_column: str = "comment",
    output_dir: str = "data/processed",
    max_features: int = 10000,
    min_df: int = 30,
    max_df: float = 0.8,
    export_cleaned: bool = True,
    export_tfidf: bool = True,
    export_metadata: bool = True
):
    """
    Prepare data for clustering: clean, tokenize, and vectorize.
    
    Args:
        input_file: Path to input CSV file
        text_column: Name of the text column to process
        output_dir: Directory to save output files
        max_features: Maximum number of TF-IDF features
        min_df: Minimum document frequency for terms
        max_df: Maximum document frequency for terms
        export_cleaned: Whether to export cleaned text
        export_tfidf: Whether to export TF-IDF vectors
        export_metadata: Whether to export metadata
    """
    print(f"🚀 Starting data preparation...")
    print(f"📁 Input file: {input_file}")
    print(f"📝 Text column: {text_column}")
    print(f"📊 Max features: {max_features:,}")
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Load data
    print(f"\n📥 Loading data from {input_file}...")
    start_time = time.time()
    
    if input_file.endswith('.csv'):
        df = pd.read_csv(input_file)
    elif input_file.endswith('.parquet'):
        df = pd.read_parquet(input_file)
    else:
        raise ValueError("Input file must be CSV or Parquet")
    
    print(f"✅ Loaded {len(df):,} records")
    print(f"📋 Columns: {list(df.columns)}")
    
    # Check if text column exists
    if text_column not in df.columns:
        raise ValueError(f"Text column '{text_column}' not found. Available columns: {list(df.columns)}")
    
    # Show text column statistics
    print(f"\n📊 Text column statistics:")
    print(f"  Non-null values: {df[text_column].notna().sum():,}")
    print(f"  Null values: {df[text_column].isna().sum():,}")
    print(f"  Empty strings: {(df[text_column].astype(str).str.strip() == '').sum():,}")
    
    # Clean and tokenize
    print(f"\n🔄 Cleaning and tokenizing text...")
    df_cleaned = cleanse_dataframe(df, text_col=text_column)
    
    # Show cleaning results
    non_empty = (df_cleaned["clean_joined"] != "").sum()
    print(f"✅ Cleaning complete:")
    print(f"  Non-empty cleaned texts: {non_empty:,}")
    print(f"  Empty cleaned texts: {len(df_cleaned) - non_empty:,}")
    
    # Build TF-IDF vectors
    print(f"\n🔍 Building TF-IDF vectors...")
    X, vec, df_valid, df_invalid = build_tfidf(
        df_cleaned, 
        max_features=max_features,
        min_df=min_df,
        max_df=max_df
    )
    
    # Show vectorization results
    print(f"✅ TF-IDF vectorization complete:")
    print(f"  Matrix shape: {X.shape}")
    print(f"  Valid documents: {len(df_valid):,}")
    print(f"  Invalid documents: {len(df_invalid):,}")
    
    # Export cleaned data
    if export_cleaned:
        cleaned_file = output_path / "cleaned_data.csv"
        df_cleaned.to_csv(cleaned_file, index=False)
        print(f"📁 Cleaned data saved to: {cleaned_file}")
    
    # Export TF-IDF vectors as CSV
    if export_tfidf:
        # Convert sparse matrix to dense for CSV export
        print(f"💾 Converting TF-IDF to dense matrix for CSV export...")
        X_dense = X.toarray()
        
        # Create feature names
        feature_names = vec.get_feature_names_out()
        
        # Create DataFrame with TF-IDF vectors
        tfidf_df = pd.DataFrame(X_dense, columns=feature_names)
        
        # Add document index
        tfidf_df.index = df_valid.index
        tfidf_df.index.name = "doc_id"
        
        # Save TF-IDF vectors
        tfidf_file = output_path / "tfidf_vectors.csv"
        tfidf_df.to_csv(tfidf_file)
        print(f"📁 TF-IDF vectors saved to: {tfidf_file}")
        print(f"   Shape: {tfidf_df.shape}")
        print(f"   Features: {len(feature_names)}")
    
    # Export metadata
    if export_metadata:
        # Create metadata DataFrame
        metadata_df = df_valid.copy()
        metadata_df["doc_id"] = metadata_df.index
        metadata_df["cluster"] = -1  # Placeholder for clustering
        
        # Save metadata
        metadata_file = output_path / "metadata.csv"
        metadata_df.to_csv(metadata_file, index=False)
        print(f"📁 Metadata saved to: {metadata_file}")
    
    # Export vectorizer info
    vectorizer_info = {
        "n_features": len(vec.get_feature_names_out()),
        "feature_names": list(vec.get_feature_names_out()),
        "vocabulary": vec.vocabulary_,
        "idf": vec.idf_.tolist(),
        "max_features": max_features,
        "min_df": min_df,
        "max_df": max_df
    }
    
    import json
    vectorizer_file = output_path / "vectorizer_info.json"
    with open(vectorizer_file, 'w', encoding='utf-8') as f:
        json.dump(vectorizer_info, f, ensure_ascii=False, indent=2)
    print(f"📁 Vectorizer info saved to: {vectorizer_file}")
    
    # Summary
    elapsed = time.time() - start_time
    print(f"\n✅ Data preparation complete in {elapsed:.2f}s!")
    print(f"📊 Summary:")
    print(f"  Original records: {len(df):,}")
    print(f"  Valid documents: {len(df_valid):,}")
    print(f"  TF-IDF features: {len(vec.get_feature_names_out()):,}")
    print(f"  Output directory: {output_path}")
    
    return {
        "tfidf_matrix": X,
        "vectorizer": vec,
        "valid_data": df_valid,
        "invalid_data": df_invalid,
        "output_path": output_path
    }

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Prepare data for clustering: clean, tokenize, and vectorize",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic usage with default settings
  python scripts/prepare_data.py --input data/raw/reviews.csv
  
  # Custom text column and output directory
  python scripts/prepare_data.py --input reviews.csv --text-col review_text --output processed_data
  
  # Adjust TF-IDF parameters
  python scripts/prepare_data.py --input reviews.csv --max-features 5000 --min-df 50
  
  # Export only TF-IDF vectors
  python scripts/prepare_data.py --input reviews.csv --no-cleaned --no-metadata
        """
    )
    
    parser.add_argument(
        "--input", 
        required=True,
        help="Input CSV or Parquet file path"
    )
    
    parser.add_argument(
        "--text-col", 
        default="comment",
        help="Name of the text column to process (default: comment)"
    )
    
    parser.add_argument(
        "--output", 
        default="data/processed",
        help="Output directory (default: data/processed)"
    )
    
    parser.add_argument(
        "--max-features", 
        type=int, 
        default=10000,
        help="Maximum number of TF-IDF features (default: 10000)"
    )
    
    parser.add_argument(
        "--min-df", 
        type=int, 
        default=30,
        help="Minimum document frequency for terms (default: 30)"
    )
    
    parser.add_argument(
        "--max-df", 
        type=float, 
        default=0.8,
        help="Maximum document frequency for terms (default: 0.8)"
    )
    
    parser.add_argument(
        "--no-cleaned", 
        action="store_true",
        help="Skip exporting cleaned data"
    )
    
    parser.add_argument(
        "--no-tfidf", 
        action="store_true",
        help="Skip exporting TF-IDF vectors"
    )
    
    parser.add_argument(
        "--no-metadata", 
        action="store_true",
        help="Skip exporting metadata"
    )
    
    args = parser.parse_args()
    
    try:
        result = prepare_data(
            input_file=args.input,
            text_column=args.text_col,
            output_dir=args.output,
            max_features=args.max_features,
            min_df=args.min_df,
            max_df=args.max_df,
            export_cleaned=not args.no_cleaned,
            export_tfidf=not args.no_tfidf,
            export_metadata=not args.no_metadata
        )
        
        print(f"\n🎉 Data preparation successful!")
        print(f"💡 Next step: Run clustering with:")
        print(f"   python scripts/run_kmeans.py --input {args.output}/tfidf_vectors.csv --clusters 5")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 