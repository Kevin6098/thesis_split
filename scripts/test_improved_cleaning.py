#!/usr/bin/env python3
"""
Test the improved text cleaning to ensure NaN values are handled properly.
"""

import pandas as pd
from pathlib import Path
import sys

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import DATASETS
from src.text_cleaning import cleanse_dataframe, clean_comment

def test_improved_cleaning():
    """Test the improved text cleaning on a sample of high rating data."""
    
    print("🧪 Testing improved text cleaning...")
    
    # Load a small sample of the high rating data
    high_rating_path = DATASETS["high_rating"]
    
    if not high_rating_path.exists():
        print(f"❌ Error: High rating dataset not found at {high_rating_path}")
        return
    
    print(f"📖 Loading sample from {high_rating_path}...")
    
    # Load a small sample for testing
    df_sample = pd.read_csv(high_rating_path, dtype={"shopid": str}, low_memory=False, nrows=1000)
    
    print(f"📊 Sample size: {len(df_sample):,}")
    
    # Check for NaN values before cleaning
    nan_before = df_sample["comment"].isna().sum()
    empty_before = (df_sample["comment"].astype(str).str.strip() == '').sum()
    
    print(f"📊 Before cleaning:")
    print(f"  • NaN comments: {nan_before:,}")
    print(f"  • Empty comments: {empty_before:,}")
    print(f"  • Valid comments: {len(df_sample) - nan_before - empty_before:,}")
    
    # Test individual comment cleaning
    print(f"\n🧪 Testing individual comment cleaning...")
    
    # Test with NaN value
    test_nan = clean_comment(pd.NA)
    print(f"  • NaN input → '{test_nan}' (length: {len(test_nan)})")
    
    # Test with empty string
    test_empty = clean_comment("")
    print(f"  • Empty input → '{test_empty}' (length: {len(test_empty)})")
    
    # Test with whitespace only
    test_whitespace = clean_comment("   \n\t   ")
    print(f"  • Whitespace input → '{test_whitespace}' (length: {len(test_whitespace)})")
    
    # Test with actual comment
    sample_comment = df_sample["comment"].dropna().iloc[0] if len(df_sample["comment"].dropna()) > 0 else "テストコメントです。"
    test_comment = clean_comment(sample_comment)
    print(f"  • Sample comment → '{test_comment[:100]}...' (length: {len(test_comment)})")
    
    # Test full dataframe cleaning
    print(f"\n🔄 Testing full dataframe cleaning...")
    df_cleaned = cleanse_dataframe(df_sample)
    
    # Check results after cleaning
    nan_after = df_cleaned["clean_joined"].isna().sum()
    empty_after = (df_cleaned["clean_joined"] == "").sum()
    non_empty_after = (df_cleaned["clean_joined"] != "").sum()
    
    print(f"📊 After cleaning:")
    print(f"  • NaN cleaned comments: {nan_after:,}")
    print(f"  • Empty cleaned comments: {empty_after:,}")
    print(f"  • Non-empty cleaned comments: {non_empty_after:,}")
    
    # Show some examples
    print(f"\n👀 Sample cleaned comments:")
    non_empty_samples = df_cleaned[df_cleaned["clean_joined"] != ""].head(3)
    for i, (_, row) in enumerate(non_empty_samples.iterrows(), 1):
        original = row["comment"][:100] + "..." if len(str(row["comment"])) > 100 else str(row["comment"])
        cleaned = row["clean_joined"]
        print(f"  {i}. Original: '{original}'")
        print(f"     Cleaned: '{cleaned}'")
        print()
    
    # Save test results
    output_path = Path("data/processed/test_cleaned_sample.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df_cleaned.to_csv(output_path, index=False)
    print(f"✅ Test results saved to {output_path}")
    
    return df_cleaned

if __name__ == "__main__":
    test_improved_cleaning() 