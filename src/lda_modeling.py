# src/lda_modeling.py
# -------------------------------------
"""
Fit LDA on the cleaned text for topic modeling.
"""
from __future__ import annotations
import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path
from joblib import dump

def fit_lda(
    df: pd.DataFrame,
    n_topics: int = 8,
    model_path: Path = Path("models") / "lda_model.pkl",
    max_features: int = 20_000,
    ngram_range: tuple[int, int] = (1, 2)
) -> tuple[LatentDirichletAllocation, CountVectorizer]:
    """
    Vectorise `clean_joined` using CountVectorizer,
    fit an LDA model, and save both vectoriser & model.
    Returns the (lda, vectoriser) tuple.
    """
    vec = CountVectorizer(
        max_features=max_features,
        ngram_range=ngram_range,
        token_pattern=r"(?u)\b\w+\b",
        min_df=30,  # Increased to suppress rare terms
        max_df=0.8  # Reduced to suppress overly common terms
    )
    X = vec.fit_transform(df["clean_joined"].values)

    # Use asymmetric alpha for sparser topic distributions
    doc_topic_prior = 0.1  # Document-topic prior (alpha)
    topic_word_prior = 0.01  # Topic-word prior (beta)
    
    lda = LatentDirichletAllocation(
        n_components=n_topics,
        random_state=42,
        learning_method="batch",
        doc_topic_prior=doc_topic_prior,
        topic_word_prior=topic_word_prior
    )
    lda.fit(X)
    dump((lda, vec), model_path)
    return lda, vec

def display_topics(
    lda: LatentDirichletAllocation,
    vec: CountVectorizer,
    n_top_words: int = 10
) -> dict[int, list[str]]:
    """
    Print and return the top words for each LDA topic.
    """
    feature_names = vec.get_feature_names_out()
    topics: dict[int, list[str]] = {}
    for idx, comp in enumerate(lda.components_):
        terms = [
            feature_names[i]
            for i in comp.argsort()[-n_top_words:][::-1]
        ]
        topics[idx] = terms
        print(f"Topic {idx}: {', '.join(terms)}")
    return topics