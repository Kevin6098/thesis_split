#!/usr/bin/env python3
"""
Export cleaned high rating dataset with improved text cleaning.

This script applies the improved text cleaning (handling NaN values and spacing)
to the full high rating dataset and exports the results.
"""

import pandas as pd
from pathlib import Path
import sys

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import DATASETS, DATA_DIR
from src.text_cleaning import cleanse_dataframe

def export_cleaned_high_rating():
    """Export cleaned high rating dataset with improved text cleaning."""
    
    print("📊 Exporting cleaned high rating dataset...")
    
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
    
    # Export cleaned dataset
    output_path = DATA_DIR / "processed" / "high_rating_cleaned_improved.csv"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    df_cleaned.to_csv(output_path, index=False)
    
    print(f"✅ Exported cleaned dataset to {output_path}")
    
    # Show final statistics
    total_records = len(df_cleaned)
    non_empty_comments = (df_cleaned["clean_joined"] != "").sum()
    empty_comments = (df_cleaned["clean_joined"] == "").sum()
    
    print(f"\n📈 Final Statistics:")
    print(f"  • Total records: {total_records:,}")
    print(f"  • Non-empty cleaned comments: {non_empty_comments:,} ({non_empty_comments/total_records*100:.1f}%)")
    print(f"  • Empty cleaned comments: {empty_comments:,} ({empty_comments/total_records*100:.1f}%)")
    
    # Show sample of cleaned comments
    print(f"\n👀 Sample cleaned comments:")
    non_empty_samples = df_cleaned[df_cleaned["clean_joined"] != ""].head(3)
    for i, (_, row) in enumerate(non_empty_samples.iterrows(), 1):
        original = row["comment"][:100] + "..." if len(str(row["comment"])) > 100 else str(row["comment"])
        cleaned = row["clean_joined"][:200] + "..." if len(row["clean_joined"]) > 200 else row["clean_joined"]
        print(f"  {i}. Original: '{original}'")
        print(f"     Cleaned: '{cleaned}'")
        print()
    
    # Also save as parquet for faster loading
    parquet_path = DATA_DIR / "processed" / "high_rating_cleaned_improved.parquet"
    df_cleaned.to_parquet(parquet_path, index=False)
    print(f"✅ Also saved as parquet: {parquet_path}")
    
    return df_cleaned

if __name__ == "__main__":
    export_cleaned_high_rating() 