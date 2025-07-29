from pathlib import Path
from sklearn.cluster import KMeans
from joblib import dump
import pandas as pd
import numpy as np

def fit_kmeans(X, k: int, model_path: Path):
    print(f"🔄 Fitting K-means with k={k}...")
    km = KMeans(n_clusters=k, n_init="auto", random_state=42)
    km.fit(X)
    dump(km, model_path)
    print(f"✅ K-means model saved to {model_path}")
    return km

def apply_clustering_with_invalid_handling(df: pd.DataFrame, k: int, model_path: Path):
    """
    Apply clustering while properly handling invalid (empty/NaN) documents.
    
    Args:
        df: DataFrame with 'clean_joined' column
        k: number of clusters
        model_path: path to save the model
    
    Returns:
        df_with_clusters: DataFrame with cluster labels for all documents
    """
    from src.vectorize import build_tfidf
    
    print(f"🔄 Building TF-IDF and applying clustering with k={k}...")
    
    # Build TF-IDF (this now returns valid and invalid dataframes)
    X, vec, df_valid, df_invalid = build_tfidf(df)
    
    # Fit K-means on valid documents only
    km = fit_kmeans(X, k, model_path)
    
    # Get cluster labels for valid documents
    valid_labels = km.labels_
    df_valid["cluster"] = valid_labels
    
    # Assign a special cluster label (-1) to invalid documents
    df_invalid["cluster"] = -1
    
    # Combine the dataframes
    df_with_clusters = pd.concat([df_valid, df_invalid], ignore_index=True)
    
    # Sort by original index to maintain order
    df_with_clusters = df_with_clusters.sort_index()
    
    # Show cluster distribution
    print("\n📊 Cluster distribution:")
    cluster_counts = df_with_clusters["cluster"].value_counts().sort_index()
    for cluster, count in cluster_counts.items():
        if cluster == -1:
            print(f"  Invalid documents: {count:,} records ({count/len(df_with_clusters)*100:.1f}%)")
        else:
            print(f"  Cluster {cluster}: {count:,} records ({count/len(df_with_clusters)*100:.1f}%)")
    
    return df_with_clusters