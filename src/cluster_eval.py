import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from tqdm import tqdm

def best_k_silhouette(X, k_min=2, k_max=10, random_state=42):
    print("🔄 Evaluating optimal k using silhouette scores...")
    scores = {}
    for k in tqdm(range(k_min, k_max + 1), desc="Testing k values", unit="k"):
        km = KMeans(n_clusters=k, n_init="auto", random_state=random_state)
        labels = km.fit_predict(X)
        score  = silhouette_score(X, labels)
        scores[k] = score
        print(f"  k={k:2d} → silhouette={score:.4f}")
    best_k = max(scores, key=scores.get)
    print(f"✅ Best k: {best_k} (silhouette={scores[best_k]:.4f})")
    print("\n--- Silhouette Scores by k ---")
    for k in sorted(scores):
        print(f"k={k:2d} : silhouette={scores[k]:.4f}")
    print("-----------------------------\n")
    return best_k, scores