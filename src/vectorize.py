import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def build_tfidf(df: pd.DataFrame, max_features: int = 20_000):
    vec = TfidfVectorizer(max_features=max_features)
    X   = vec.fit_transform(df["clean_joined"].values)
    return X, vec