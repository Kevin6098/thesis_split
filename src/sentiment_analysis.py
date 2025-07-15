# src/sentiment_analysis.py
# -------------------------------------
from __future__ import annotations
import pandas as pd
from pathlib import Path
from .topic_inspection import _NEG_KEYWORDS

def score_sentiment_rule(
    df: pd.DataFrame,
    text_col: str = "clean_joined"
) -> pd.DataFrame:
    """
    Rule-based sentiment:
    - Label 'negative' if any keyword in _NEG_KEYWORDS appears.
    - Otherwise 'positive'.
    Also computes a simple score = (# negative tokens) / (total tokens).
    """
    df = df.copy()

    def is_negative(txt: str) -> bool:
        return any(kw in txt for kw in _NEG_KEYWORDS)

    def negative_score(txt: str) -> float:
        toks = txt.split()
        if not toks:
            return 0.0
        return sum(1 for t in toks if t in _NEG_KEYWORDS) / len(toks)

    df["sentiment_label"] = df[text_col].map(
        lambda s: "negative" if is_negative(s) else "positive"
    )
    df["sentiment_score"] = df[text_col].map(negative_score)
    return df

def save_sentiment(df: pd.DataFrame, slug: str) -> Path:
    """
    Apply rule-based sentiment and save to parquet.
    """
    scored = score_sentiment_rule(df)
    out = Path("data/processed") / f"{slug}_sentiment.parquet"
    scored.to_parquet(out, index=False)
    return out