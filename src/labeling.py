import pandas as pd
from .config import HIGH_RATING_QUANTILE, HIGH_COMMENT_QUANTILE

HIGH_RATING  = "high_rating"
HIGH_COMMENT = "high_comment"
SEGMENT      = "segment"

def add_labels(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    r_thr = df["rating"].quantile(HIGH_RATING_QUANTILE)
    c_thr = df["n_reviews"].quantile(HIGH_COMMENT_QUANTILE)
    df[HIGH_RATING]  = (df["rating"]    >= r_thr).astype(int)
    df[HIGH_COMMENT] = (df["n_reviews"] >= c_thr).astype(int)
    df[SEGMENT] = (
        df[HIGH_RATING].map({1:"High★",0:"Low★"}) + " & " +
        df[HIGH_COMMENT].map({1:"High🗣",0:"Low🗣"})
    )
    return df
