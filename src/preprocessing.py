import re, unicodedata
import pandas as pd
from .config import DATA_DIR

_FULLWIDTH = re.compile(r"[Ａ-Ｚａ-ｚ０-９]+")

def _to_halfwidth(s: str) -> str:
    return unicodedata.normalize("NFKC", s)

"""Clean numeric & compute unified 'rating' and rename visits→n_reviews."""

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    # half-width conversion for text cols
    for col in df.select_dtypes("object"):
        df[col] = df[col].astype(str).map(_to_halfwidth)
    # rename
    df.rename(columns={"visits": "n_reviews"}, inplace=True)
    # rating = mean of dinner & lunch overall scores
    df["rating"] = df[["overall_dinner","overall_lunch"]].mean(axis=1)
    # numeric fill for price & ratings
    num_cols = ["price","n_reviews","rating"]
    df[num_cols] = df[num_cols].fillna(df[num_cols].median())
    return df
