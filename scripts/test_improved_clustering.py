#!/usr/bin/env python3
"""
Test the improved clustering to ensure NaN values are properly handled.
"""

import pandas as pd
from pathlib import Path
import sys

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import DATASETS, DATA_DIR
from src.text_cleaning import cleanse_dataframe
from src.clustering import apply_clustering_with_invalid_handling

def test_improved_clustering():
    """Test the improved clustering on a sample of high rating data."""
    
    print("🧪 Testing improved clustering...")
    
    # Load a small sample of the high rating data
    high_rating_path = DATASETS["high_rating"]
    
    if not high_rating_path.exists():
        print(f"❌ Error: High rating dataset not found at {high_rating_path}")
        return
    
    print(f"📖 Loading sample from {high_rating_path}...")
    
    # Load a small sample for testing
    df_sample = pd.read_csv(high_rating_path, dtype={"shopid": str}, low_memory=False, nrows=2000)
    
    print(f"📊 Sample size: {len(df_sample):,}")
    
    # Apply improved text cleaning
    print("🔄 Applying improved text cleaning...")
    df_cleaned = cleanse_dataframe(df_sample, text_col="comment")
    
    # Check for empty/NaN values after cleaning
    empty_after = (df_cleaned["clean_joined"] == "").sum()
    nan_after = df_cleaned["clean_joined"].isna().sum()
    valid_after = (df_cleaned["clean_joined"] != "").sum()
    
    print(f"📊 After cleaning:")
    print(f"  • Empty cleaned comments: {empty_after:,}")
    print(f"  • NaN cleaned comments: {nan_after:,}")
    print(f"  • Valid cleaned comments: {valid_after:,}")
    
    # Test improved clustering
    print(f"\n🔄 Testing improved clustering...")
    model_path = DATA_DIR / "models" / "test_improved_clustering.pkl"
    model_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_clustered = apply_clustering_with_invalid_handling(df_cleaned, k=3, model_path=model_path)
    
    # Check cluster distribution
    print(f"\n📊 Final cluster distribution:")
    cluster_counts = df_clustered["cluster"].value_counts().sort_index()
    for cluster, count in cluster_counts.items():
        if cluster == -1:
            print(f"  • Invalid documents: {count:,} ({count/len(df_clustered)*100:.1f}%)")
        else:
            print(f"  • Cluster {cluster}: {count:,} ({count/len(df_clustered)*100:.1f}%)")
    
    # Check if there are any "nan" clusters
    nan_clusters = df_clustered[df_clustered["cluster"] == "nan"]
    if len(nan_clusters) > 0:
        print(f"⚠️  Warning: Found {len(nan_clusters)} documents with 'nan' cluster labels")
    else:
        print(f"✅ No 'nan' cluster labels found!")
    
    # Show sample of each cluster
    print(f"\n👀 Sample documents from each cluster:")
    for cluster in sorted(df_clustered["cluster"].unique()):
        cluster_docs = df_clustered[df_clustered["cluster"] == cluster].head(2)
        if cluster == -1:
            print(f"  Invalid documents (cluster -1):")
        else:
            print(f"  Cluster {cluster}:")
        
        for i, (_, row) in enumerate(cluster_docs.iterrows(), 1):
            comment_preview = row["comment"][:100] + "..." if len(str(row["comment"])) > 100 else str(row["comment"])
            cleaned_preview = row["clean_joined"][:50] + "..." if len(row["clean_joined"]) > 50 else row["clean_joined"]
            print(f"    {i}. Comment: '{comment_preview}'")
            print(f"       Cleaned: '{cleaned_preview}'")
            print()
    
    # Save test results
    output_path = DATA_DIR / "processed" / "test_improved_clustering.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_clustered.to_csv(output_path, index=False)
    print(f"✅ Test results saved to {output_path}")
    
    return df_clustered

if __name__ == "__main__":
    test_improved_clustering() 