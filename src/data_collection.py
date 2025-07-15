import pandas as pd
from pathlib import Path

"""Load raw CSV into DataFrame (expects the exact header)."""

def load_raw(path: Path) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"CSV not found at {path}")
    df = pd.read_csv(path, dtype={"id": str, "restaurant_id": str}, low_memory=False)
    # ensure required columns present
    req = {"id","restaurant_id","visits","comment","overall_dinner","overall_lunch"}
    missing = req - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    return df
