from collections import Counter
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

_NEG_KEYWORDS = {
    "高い", "遅い", "最悪", "残念", "不味い", "ひどい", "汚い",
    "小さい", "高過ぎ", "塩辛い",
}

def flag_negative(s: str) -> bool:
    return any(kw in s for kw in _NEG_KEYWORDS)

def extract_ngrams(texts, n=2, top=10):
    vec   = CountVectorizer(max_features=10_000, ngram_range=(1, n))
    X     = vec.fit_transform(texts)
    total = X.sum(axis=0).A1
    vocab = np.array(vec.get_feature_names_out())
    pairs = sorted(zip(vocab, total), key=lambda t: t[1], reverse=True)
    return pairs[:top]

def summarise_cluster(df: pd.DataFrame, cluster_id: int):
    cl_df  = df[df["cluster"] == cluster_id]
    neg_df = cl_df[cl_df["clean_joined"].map(flag_negative)]

    phrases  = extract_ngrams(neg_df["clean_joined"].tolist(), n=2, top=10)
    examples = cl_df.head(5)[["comment", "clean_joined"]]

    return phrases, examples