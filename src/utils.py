from pathlib import Path
import pandas as pd

def ensure_dir(p: Path):
    p.mkdir(parents=True, exist_ok=True)

def describe_by_group(df: pd.DataFrame, group_col: str, target: str):
    return (
        df.groupby(group_col)[target]
          .agg(["count", "mean", "median", "std"])
          .sort_values("count", ascending=False)
    )