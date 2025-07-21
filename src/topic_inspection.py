"""
src/topic_inspection.py
-----------------------
Utilities for drilling down into a single *cluster*:
•  flag_negative  … simple keyword–based negative‐sentiment flag
•  extract_ngrams … TF counts for uni/bi-grams inside the cluster
•  summarise_cluster … returns (top_phrases, sample_df)
   - top_phrases : list[(ngram, freq)]  length = `top`
   - sample_df   : DataFrame[["comment", "clean_joined"]]
"""

from collections import Counter
from pathlib import Path
from typing import List, Tuple

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from numpy.random import default_rng

# -------------------------- 1. negative flagger ---------------------------- #

_NEG_KEYWORDS: set[str] = {
    "高い", "遅い", "最悪", "残念", "不味い", "ひどい", "汚い",
    "小さい", "高過ぎ", "塩辛い", "コスパ悪い", "サービス悪い",
}


def flag_negative(s: str) -> bool:
    """Return True if any negative keyword is found in the string."""
    return any(kw in s for kw in _NEG_KEYWORDS)


# -------------------------- 2. n-gram extractor ---------------------------- #

def extract_ngrams(texts: List[str], *, n: int = 2, top: int = 10
                   ) -> List[Tuple[str, int]]:
    """
    Return the `top` most frequent uni/bi-grams in `texts`.

    Parameters
    ----------
    texts : list[str]
    n     : max n-gram length (default 2 → unigrams+bigrams)
    top   : how many phrases to return
    """
    if not texts:
        return []

    vec = CountVectorizer(
        max_features=20_000,
        ngram_range=(1, n),
        token_pattern=r"(?u)\b\w+\b"   # works for latin & kana/kanji split済み
    )
    X = vec.fit_transform(texts)
    total = X.sum(axis=0).A1
    vocab = np.array(vec.get_feature_names_out())
    pairs = sorted(zip(vocab, total), key=lambda t: t[1], reverse=True)
    return pairs[:top]


# -------------------------- 3. cluster summary ----------------------------- #

_rng = default_rng()


def summarise_cluster(df: pd.DataFrame, cid: int,
                      n_samples: int = 5, ngram_top: int = 10
                      ) -> Tuple[List[Tuple[str, int]], pd.DataFrame]:
    """
    Parameters
    ----------
    df : DataFrame  (must contain 'cluster', 'comment', 'clean_joined')
    cid : target cluster id
    n_samples : how many example reviews to return
    ngram_top : how many top n-grams to return

    Returns
    -------
    phrases : list of (ngram, freq) tuples (length <= ngram_top)
    examples : DataFrame[["comment", "clean_joined"]] length = n_samples
    """

    cl_df = df[df["cluster"] == cid]
    if cl_df.empty:
        return [], pd.DataFrame(columns=["comment", "clean_joined"])

    # 1) pick negative subset for phrase mining
    neg_df = cl_df[cl_df["clean_joined"].map(flag_negative)]
    src_texts = (neg_df if not neg_df.empty else cl_df)["clean_joined"].tolist()

    phrases = extract_ngrams(src_texts, n=2, top=ngram_top)

    # 2) sample example reviews (random for variety)
    if len(cl_df) <= n_samples:
        examples = cl_df[["comment", "clean_joined"]]
    else:
        idx = _rng.choice(cl_df.index, size=n_samples, replace=False)
        examples = cl_df.loc[idx, ["comment", "clean_joined"]]

    return phrases, examples.reset_index(drop=True)