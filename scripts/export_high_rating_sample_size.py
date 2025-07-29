#!/usr/bin/env python3
"""
Export high rating sample size information to CSV.

This script loads the high rating dataset and exports sample size statistics
to a CSV file for analysis.
"""

import pandas as pd
from pathlib import Path
import sys

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import DATASETS

def export_high_rating_sample_size():
    """Export high rating sample size information to CSV."""
    
    print("📊 Exporting high rating sample size information...")
    
    # Load the high rating dataset
    high_rating_path = DATASETS["high_rating"]
    
    if not high_rating_path.exists():
        print(f"❌ Error: High rating dataset not found at {high_rating_path}")
        return
    
    print(f"📖 Loading data from {high_rating_path}...")
    
    # Load the data
    df = pd.read_csv(high_rating_path, dtype={"shopid": str}, low_memory=False)
    
    # Basic sample size information
    total_records = len(df)
    
    # Create sample size summary
    sample_info = {
        "dataset": ["high_rating"],
        "total_records": [total_records],
        "file_size_mb": [high_rating_path.stat().st_size / (1024 * 1024)],
        "columns": [len(df.columns)],
        "memory_usage_mb": [df.memory_usage(deep=True).sum() / (1024 * 1024)]
    }
    
    # Add column-specific information
    if "comment" in df.columns:
        sample_info["non_null_comments"] = [df["comment"].notna().sum()]
        sample_info["null_comments"] = [df["comment"].isna().sum()]
        sample_info["avg_comment_length"] = [df["comment"].str.len().mean()]
    
    if "overall_dinner" in df.columns:
        sample_info["dinner_ratings"] = [df["overall_dinner"].notna().sum()]
    
    if "overall_lunch" in df.columns:
        sample_info["lunch_ratings"] = [df["overall_lunch"].notna().sum()]
    
    # Create DataFrame
    sample_df = pd.DataFrame(sample_info)
    
    # Round numeric columns
    numeric_cols = sample_df.select_dtypes(include=['float64']).columns
    sample_df[numeric_cols] = sample_df[numeric_cols].round(2)
    
    # Export to CSV
    output_path = Path("data/processed/high_rating_sample_size.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    sample_df.to_csv(output_path, index=False)
    
    print(f"✅ Exported sample size information to {output_path}")
    print(f"📊 Total records: {total_records:,}")
    print(f"💾 File size: {sample_info['file_size_mb'][0]:.2f} MB")
    print(f"🧠 Memory usage: {sample_info['memory_usage_mb'][0]:.2f} MB")
    
    return sample_df

if __name__ == "__main__":
    export_high_rating_sample_size() 