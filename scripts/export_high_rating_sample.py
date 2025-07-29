#!/usr/bin/env python3
"""
Export a random sample of 1,000 reviews from high rating comments to CSV.

This script loads the high rating dataset, takes a random sample of 1,000 reviews,
and exports them to a CSV file for preview purposes.
"""

import pandas as pd
from pathlib import Path
import sys

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import DATASETS

def export_high_rating_sample(sample_size=1000, random_state=42):
    """Export a random sample of high rating reviews to CSV."""
    
    print(f"📊 Exporting random sample of {sample_size:,} reviews from high rating dataset...")
    
    # Load the high rating dataset
    high_rating_path = DATASETS["high_rating"]
    
    if not high_rating_path.exists():
        print(f"❌ Error: High rating dataset not found at {high_rating_path}")
        return
    
    print(f"📖 Loading data from {high_rating_path}...")
    
    # Load the data
    df = pd.read_csv(high_rating_path, dtype={"shopid": str}, low_memory=False)
    
    print(f"📊 Total records in dataset: {len(df):,}")
    
    # Take a random sample
    df_sample = df.sample(n=min(sample_size, len(df)), random_state=random_state)
    
    print(f"🎲 Selected {len(df_sample):,} random reviews")
    
    # Export to CSV
    output_path = Path("data/processed/high_rating_sample_1000.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_sample.to_csv(output_path, index=False)
    
    print(f"✅ Exported sample to {output_path}")
    
    # Show sample statistics
    print(f"\n📈 Sample Statistics:")
    print(f"  • Total reviews: {len(df_sample):,}")
    print(f"  • Reviews with comments: {df_sample['comment'].notna().sum():,}")
    print(f"  • Reviews without comments: {df_sample['comment'].isna().sum():,}")
    
    if 'overall_dinner' in df_sample.columns:
        print(f"  • Dinner ratings: {df_sample['overall_dinner'].notna().sum():,}")
    
    if 'overall_lunch' in df_sample.columns:
        print(f"  • Lunch ratings: {df_sample['overall_lunch'].notna().sum():,}")
    
    # Show column names for reference
    print(f"\n📋 Columns in the sample:")
    for i, col in enumerate(df_sample.columns, 1):
        print(f"  {i:2d}. {col}")
    
    # Show first few rows as preview
    print(f"\n👀 Sample preview (first 3 rows):")
    print(df_sample.head(3).to_string(max_cols=10, max_colwidth=50))
    
    return df_sample

if __name__ == "__main__":
    export_high_rating_sample() 