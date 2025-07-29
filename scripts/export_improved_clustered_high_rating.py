#!/usr/bin/env python3
"""
Export improved clustered high rating dataset.

This script applies the improved clustering (properly handling NaN values)
to the full high rating dataset and exports the results.
"""

import pandas as pd
from pathlib import Path
import sys

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import DATASETS, DATA_DIR
from src.text_cleaning import cleanse_dataframe
from src.clustering import apply_clustering_with_invalid_handling

def export_improved_clustered_high_rating():
    """Export improved clustered high rating dataset."""
    
    print("📊 Exporting improved clustered high rating dataset...")
    
    # Load the high rating dataset
    high_rating_path = DATASETS["high_rating"]
    
    if not high_rating_path.exists():
        print(f"❌ Error: High rating dataset not found at {high_rating_path}")
        return
    
    print(f"📖 Loading data from {high_rating_path}...")
    
    # Load the data
    df = pd.read_csv(high_rating_path, dtype={"shopid": str}, low_memory=False)
    
    print(f"📊 Original dataset size: {len(df):,}")
    
    # Apply improved text cleaning
    print("🔄 Applying improved text cleaning...")
    df_cleaned = cleanse_dataframe(df, text_col="comment")
    
    # Apply improved clustering
    print("🔄 Applying improved clustering...")
    model_path = DATA_DIR / "models" / "high_rating_improved_clustering.pkl"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Use k=8 based on previous analysis
    df_clustered = apply_clustering_with_invalid_handling(df_cleaned, k=8, model_path=model_path)
    
    # Export clustered dataset
    output_path = DATA_DIR / "processed" / "high_rating_improved_clustered.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_clustered.to_csv(output_path, index=False)
    
    print(f"✅ Exported improved clustered dataset to {output_path}")
    
    # Also save as parquet for faster loading
    parquet_path = DATA_DIR / "processed" / "high_rating_improved_clustered.parquet"
    df_clustered.to_parquet(parquet_path, index=False)
    print(f"✅ Also saved as parquet: {parquet_path}")
    
    # Show final statistics
    total_records = len(df_clustered)
    invalid_docs = (df_clustered["cluster"] == -1).sum()
    valid_clusters = df_clustered[df_clustered["cluster"] != -1]["cluster"].nunique()
    
    print(f"\n📈 Final Statistics:")
    print(f"  • Total records: {total_records:,}")
    print(f"  • Invalid documents (cluster -1): {invalid_docs:,} ({invalid_docs/total_records*100:.1f}%)")
    print(f"  • Valid clusters: {valid_clusters}")
    print(f"  • Valid documents: {total_records - invalid_docs:,} ({(total_records - invalid_docs)/total_records*100:.1f}%)")
    
    # Show cluster distribution
    print(f"\n📊 Cluster distribution:")
    cluster_counts = df_clustered["cluster"].value_counts().sort_index()
    for cluster, count in cluster_counts.items():
        if cluster == -1:
            print(f"  • Invalid documents: {count:,} ({count/total_records*100:.1f}%)")
        else:
            print(f"  • Cluster {cluster}: {count:,} ({count/total_records*100:.1f}%)")
    
    # Check if there are any "nan" clusters
    nan_clusters = df_clustered[df_clustered["cluster"] == "nan"]
    if len(nan_clusters) > 0:
        print(f"⚠️  Warning: Found {len(nan_clusters)} documents with 'nan' cluster labels")
    else:
        print(f"✅ No 'nan' cluster labels found!")
    
    return df_clustered

if __name__ == "__main__":
    export_improved_clustered_high_rating() 