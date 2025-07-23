from pathlib import Path
from sklearn.cluster import KMeans
from joblib import dump

def fit_kmeans(X, k: int, model_path: Path):
    print(f"🔄 Fitting K-means with k={k}...")
    km = KMeans(n_clusters=k, n_init="auto", random_state=42)
    km.fit(X)
    dump(km, model_path)
    print(f"✅ K-means model saved to {model_path}")
    return km