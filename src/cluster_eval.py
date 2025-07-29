import numpy as np
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from tqdm import tqdm
import time

def sampled_silhouette_score(X, labels, sample_size=100000, random_state=42):
    """
    Calculate silhouette score using a sample of the data for faster computation.
    
    Args:
        X: Feature matrix
        labels: Cluster labels
        sample_size: Number of samples to use for calculation (default: 100k)
        random_state: Random seed for sampling
    
    Returns:
        Approximate silhouette score
    """
    n_samples = X.shape[0]  # Use shape[0] for sparse matrices
    if n_samples <= sample_size:
        return silhouette_score(X, labels)
    
    # Sample data for faster computation
    np.random.seed(random_state)
    indices = np.random.choice(n_samples, sample_size, replace=False)
    X_sample = X[indices]
    labels_sample = labels[indices]
    
    return silhouette_score(X_sample, labels_sample)

def best_k_silhouette(X, k_min=2, k_max=10, random_state=42, use_sampling=True, sample_size=100000):
    """
    Evaluate optimal k using silhouette scores with optional sampling for speed.
    
    Args:
        X: Feature matrix
        k_min: Minimum k value
        k_max: Maximum k value
        random_state: Random seed
        use_sampling: Whether to use sampling for silhouette calculation
        sample_size: Sample size for silhouette calculation (default: 100k)
    """
    print("🔄 Evaluating optimal k using silhouette scores...")
    if use_sampling:
        print(f"🎲 Using sampling (sample_size={sample_size:,}) for faster computation")
    
    scores = {}
    start_time = time.time()
    
    for k in tqdm(range(k_min, k_max + 1), desc="Testing k values", unit="k"):
        # Use regular KMeans
        km = KMeans(
            n_clusters=k, 
            random_state=random_state,
            n_init="auto"
        )
        labels = km.fit_predict(X)
        
        # Calculate silhouette score
        if use_sampling:
            score = sampled_silhouette_score(X, labels, sample_size, random_state)
        else:
            score = silhouette_score(X, labels)
        
        scores[k] = score
        print(f"  k={k:2d} → silhouette={score:.4f}")
    
    elapsed = time.time() - start_time
    best_k = max(scores, key=scores.get)
    print(f"✅ Best k: {best_k} (silhouette={scores[best_k]:.4f})")
    print(f"⏱️  Evaluation completed in {elapsed:.2f}s")
    
    print("\n--- Silhouette Scores by k ---")
    for k in sorted(scores):
        print(f"k={k:2d} : silhouette={scores[k]:.4f}")
    print("-----------------------------\n")
    
    return best_k, scores

def fast_best_k_silhouette(X, k_min=2, k_max=10, random_state=42, sample_size=100000):
    """
    Fast version using sampling for both clustering and silhouette calculation.
    
    Args:
        X: Feature matrix
        k_min: Minimum k value
        k_max: Maximum k value
        random_state: Random seed
        sample_size: Sample size for both clustering and silhouette (default: 100k)
    """
    print("🚀 Fast k evaluation using sampling...")
    print(f"🎲 Sample size: {sample_size:,} records")
    
    # Take a sample for faster evaluation
    n_samples = X.shape[0]  # Use shape[0] for sparse matrices
    if n_samples > sample_size:
        np.random.seed(random_state)
        indices = np.random.choice(n_samples, sample_size, replace=False)
        X_sample = X[indices]
        print(f"📊 Using sample of {X_sample.shape[0]:,} records from {n_samples:,} total")
    else:
        X_sample = X
        print(f"📊 Using full dataset ({n_samples:,} records)")
    
    scores = {}
    start_time = time.time()
    
    for k in tqdm(range(k_min, k_max + 1), desc="Testing k values", unit="k"):
        # Use regular KMeans on sample
        km = KMeans(
            n_clusters=k, 
            random_state=random_state,
            n_init="auto"
        )
        labels = km.fit_predict(X_sample)
        
        # Calculate silhouette on sample
        score = silhouette_score(X_sample, labels)
        scores[k] = score
        print(f"  k={k:2d} → silhouette={score:.4f}")
    
    elapsed = time.time() - start_time
    best_k = max(scores, key=scores.get)
    print(f"✅ Best k: {best_k} (silhouette={scores[best_k]:.4f})")
    print(f"⏱️  Fast evaluation completed in {elapsed:.2f}s")
    
    print("\n--- Silhouette Scores by k ---")
    for k in sorted(scores):
        print(f"k={k:2d} : silhouette={scores[k]:.4f}")
    print("-----------------------------\n")
    
    return best_k, scores

def parallel_best_k_silhouette(X, k_min=2, k_max=10, random_state=42, sample_size=100000, n_jobs=-1):
    """
    Parallel version for even faster evaluation.
    
    Args:
        X: Feature matrix
        k_min: Minimum k value
        k_max: Maximum k value
        random_state: Random seed
        sample_size: Sample size for silhouette calculation (default: 100k)
        n_jobs: Number of parallel jobs (-1 for all CPUs)
    """
    import multiprocessing as mp
    from functools import partial
    
    print("⚡ Parallel k evaluation...")
    print(f"🎲 Sample size: {sample_size:,}")
    print(f"🔧 Parallel jobs: {n_jobs if n_jobs > 0 else mp.cpu_count()}")
    
    def evaluate_single_k(k, X_data, sample_sz, rs):
        """Evaluate a single k value."""
        np.random.seed(rs)
        
        # Use regular KMeans for clustering
        km = KMeans(
            n_clusters=k, 
            random_state=rs,
            n_init="auto"
        )
        
        # Fit on sample for speed
        n_samples = X_data.shape[0]  # Use shape[0] for sparse matrices
        if n_samples > sample_sz:
            sample_indices = np.random.choice(n_samples, sample_sz, replace=False)
            X_sample = X_data[sample_indices]
        else:
            X_sample = X_data
        
        labels = km.fit_predict(X_sample)
        score = silhouette_score(X_sample, labels)
        
        return k, score
    
    # Prepare function for parallel processing
    eval_func = partial(evaluate_single_k, X_data=X, sample_sz=sample_size, rs=random_state)
    k_values = list(range(k_min, k_max + 1))
    
    # Run in parallel
    start_time = time.time()
    with mp.Pool(processes=n_jobs if n_jobs > 0 else mp.cpu_count()) as pool:
        results = pool.map(eval_func, k_values)
    
    # Organize results
    scores = {k: score for k, score in results}
    elapsed = time.time() - start_time
    
    best_k = max(scores, key=scores.get)
    print(f"✅ Best k: {best_k} (silhouette={scores[best_k]:.4f})")
    print(f"⏱️  Parallel evaluation completed in {elapsed:.2f}s")
    
    print("\n--- Silhouette Scores by k ---")
    for k in sorted(scores):
        print(f"k={k:2d} : silhouette={scores[k]:.4f}")
    print("-----------------------------\n")
    
    return best_k, scores