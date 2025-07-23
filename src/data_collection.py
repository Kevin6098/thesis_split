import pandas as pd
from pathlib import Path

"""Load raw CSV into DataFrame (expects the exact header)."""

def load_raw(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found at {path}")
    
    print(f"📖 Reading CSV from {path}...")
    df = pd.read_csv(path, dtype={"shopid": str}, low_memory=False)
    print(f"📊 Raw data shape: {df.shape}")
    
    # Rename shopid to restaurant_id to match expected column names
    if "shopid" in df.columns:
        df = df.rename(columns={"shopid": "restaurant_id"})
    
    # Add an id column if it doesn't exist (using index)
    if "id" not in df.columns:
        df["id"] = df.index.astype(str)
    
    # ensure required columns present
    req = {"id","restaurant_id","visits","comment","overall_dinner","overall_lunch"}
    missing = req - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df
