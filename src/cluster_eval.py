import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def best_k_silhouette(X, k_min=2, k_max=10, random_state=42):
    scores = {}
    for k in range(k_min, k_max + 1):
        km = KMeans(n_clusters=k, n_init="auto", random_state=random_state)
        labels = km.fit_predict(X)
        score  = silhouette_score(X, labels)
        scores[k] = score
        print(f"k={k:2d} → silhouette={score:.4f}")
    best_k = max(scores, key=scores.get)
    return best_k, scores