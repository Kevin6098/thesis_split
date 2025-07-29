import time
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from src.stop_words import STOP_WORDS

def build_tfidf(
    df: pd.DataFrame,
    max_features: int = 10_000,  # Reduced from 20_000
    min_df: int = 30,            # Increased from 20 to suppress rare terms
    max_df: float = 0.8          # Reduced from 0.85 to suppress overly common terms
):
    """
    Build a TF–IDF matrix with sanity checks.

    Args:
        df: DataFrame containing a 'clean_joined' column.
        max_features: max vocabulary size by TF–IDF score.
        min_df: drop tokens appearing in fewer than `min_df` docs.
        max_df: drop tokens in more than `max_df` fraction of docs.

    Returns:
        X: scipy.sparse CSR TF–IDF matrix.
        vec: the fitted TfidfVectorizer.
    """
    print("🔄 Building TF–IDF vectors...")
    
    # Filter out empty strings and NaN values
    print(f"📊 Original dataset size: {len(df):,}")
    
    # Create mask for non-empty, non-NaN clean_joined values
    valid_mask = (df["clean_joined"].notna() & 
                  (df["clean_joined"].astype(str).str.strip() != "") &
                  (df["clean_joined"] != "nan"))
    
    df_valid = df[valid_mask].copy()
    df_invalid = df[~valid_mask].copy()
    
    print(f"📊 Valid documents for TF-IDF: {len(df_valid):,}")
    print(f"📊 Invalid documents (empty/NaN): {len(df_invalid):,}")
    
    if len(df_valid) == 0:
        raise ValueError("No valid documents found for TF-IDF vectorization!")
    
    vec = TfidfVectorizer(
        max_features   = max_features,
        ngram_range    = (1, 2),               # unigrams + bigrams
        token_pattern  = r"(?u)\b\w+\b",
        min_df         = min_df,
        max_df         = max_df,
        stop_words     = list(STOP_WORDS),     # your custom Japanese stopwords
        sublinear_tf   = True,                 # 1 + log(tf)
        norm           = "l2"
    )

    # 1) fit & transform, timing
    start = time.time()
    X     = vec.fit_transform(df_valid["clean_joined"].values)
    elapsed = time.time() - start
    print(f"   • Completed in {elapsed:.2f}s")

    # 2) shape
    n_docs, n_feats = X.shape
    print(f"✅ TF–IDF matrix shape: {n_docs} docs × {n_feats} features")

    # 3) sparsity
    total_cells = n_docs * n_feats
    nonzeros    = X.nnz
    sparsity    = 1 - nonzeros / total_cells
    print(f"⚡ Sparsity: {sparsity:.2%}  ({nonzeros} non-zero entries)")

    # 4) approximate CSR memory footprint
    mem_data   = X.data.nbytes
    mem_idx    = X.indices.nbytes
    mem_indptr = X.indptr.nbytes
    total_mem  = (mem_data + mem_idx + mem_indptr) / 1e6
    print(f"💾 CSR memory footprint: {total_mem:.1f} MB")

    return X, vec, df_valid, df_invalid