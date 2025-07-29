#!/usr/bin/env python3
"""
Re-cluster Cluster 8
Performs sub-clustering within the dominant cluster 8 to break it down into meaningful sub-groups
"""

import pandas as pd
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

def load_cluster8_data():
    """Load the clustered data and extract only cluster 8."""
    data_path = Path("data/processed/high_rating_improved_clustered.parquet")
    if not data_path.exists():
        raise FileNotFoundError(f"Clustered data not found at {data_path}")
    
    df = pd.read_parquet(data_path)
    cluster8_df = df[df["cluster"] == 8].copy()
    
    print(f"📊 Cluster 8 records: {len(cluster8_df):,}")
    print(f"📊 Records with non-empty clean text: {cluster8_df['clean_joined'].notna().sum():,}")
    
    # Filter out empty clean text
    cluster8_df = cluster8_df[cluster8_df["clean_joined"].notna() & 
                             (cluster8_df["clean_joined"].str.strip() != "")].copy()
    
    print(f"📊 Final records for sub-clustering: {len(cluster8_df):,}")
    return cluster8_df

def build_tfidf_for_cluster8(cluster8_df, max_features=5000, min_df=10, max_df=0.9):
    """Build TF-IDF vectors for cluster 8 data."""
    print("🔄 Building TF-IDF vectors for cluster 8...")
    
    vec = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b\w+\b",
        min_df=min_df,
        max_df=max_df,
        sublinear_tf=True,
        norm="l2"
    )
    
    X = vec.fit_transform(cluster8_df["clean_joined"].values)
    print(f"✅ TF-IDF matrix shape: {X.shape}")
    
    return X, vec

def find_optimal_k(X, k_range=(2, 8)):
    """Find optimal number of clusters using silhouette score."""
    print(f"🔍 Finding optimal k in range {k_range}...")
    
    silhouette_scores = []
    k_values = range(k_range[0], k_range[1] + 1)
    
    for k in k_values:
        kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
        labels = kmeans.fit_predict(X)
        
        # Calculate silhouette score
        if len(np.unique(labels)) > 1:
            score = silhouette_score(X, labels)
            silhouette_scores.append(score)
            print(f"  k={k}: silhouette score = {score:.3f}")
        else:
            silhouette_scores.append(0)
            print(f"  k={k}: silhouette score = 0 (single cluster)")
    
    best_k = k_values[np.argmax(silhouette_scores)]
    best_score = max(silhouette_scores)
    
    print(f"🎯 Best k: {best_k} (silhouette score: {best_score:.3f})")
    return best_k, silhouette_scores

def perform_sub_clustering(cluster8_df, X, vec, k):
    """Perform sub-clustering on cluster 8 data."""
    print(f"🔧 Performing sub-clustering with k={k}...")
    
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    sub_cluster_labels = kmeans.fit_predict(X)
    
    # Add sub-cluster labels to dataframe
    cluster8_df = cluster8_df.copy()
    cluster8_df["sub_cluster"] = sub_cluster_labels
    
    # Save the model
    model_path = Path("models/cluster8_sub_kmeans.pkl")
    model_path.parent.mkdir(exist_ok=True)
    joblib.dump((kmeans, vec), model_path)
    print(f"💾 Sub-clustering model saved to {model_path}")
    
    return cluster8_df, kmeans

def analyze_sub_clusters(cluster8_df, vec, kmeans, top_n=10):
    """Analyze the sub-clusters within cluster 8."""
    print(f"\n📊 Sub-cluster analysis:")
    
    feature_names = vec.get_feature_names_out()
    
    for i in range(kmeans.n_clusters_):
        sub_cluster_df = cluster8_df[cluster8_df["sub_cluster"] == i]
        print(f"\n🎯 Sub-cluster {i}: {len(sub_cluster_df):,} records ({len(sub_cluster_df)/len(cluster8_df)*100:.1f}%)")
        
        # Get top terms for this sub-cluster
        cluster_center = kmeans.cluster_centers_[i]
        top_indices = cluster_center.argsort()[-top_n:][::-1]
        top_terms = [feature_names[idx] for idx in top_indices]
        top_scores = [cluster_center[idx] for idx in top_indices]
        
        print(f"  Top terms:")
        for j, (term, score) in enumerate(zip(top_terms, top_scores), 1):
            print(f"    {j:2d}. {term}: {score:.3f}")
        
        # Show sample reviews
        samples = sub_cluster_df.sample(n=min(3, len(sub_cluster_df)), random_state=42)
        print(f"  Sample reviews:")
        for _, row in samples.iterrows():
            print(f"    - {row['comment'][:100]}...")

def save_sub_clustered_data(cluster8_df):
    """Save the sub-clustered data."""
    output_path = Path("data/processed/high_rating_cluster8_subclustered.parquet")
    cluster8_df.to_parquet(output_path, index=False)
    print(f"💾 Sub-clustered data saved to {output_path}")
    return output_path

def create_visualization(cluster8_df):
    """Create visualization of sub-clusters."""
    plt.figure(figsize=(12, 8))
    
    # Sub-cluster distribution
    plt.subplot(2, 2, 1)
    sub_cluster_counts = cluster8_df["sub_cluster"].value_counts().sort_index()
    sub_cluster_counts.plot(kind='bar')
    plt.title("Sub-cluster Distribution")
    plt.xlabel("Sub-cluster ID")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=45)
    
    # Sub-cluster percentage
    plt.subplot(2, 2, 2)
    percentages = (sub_cluster_counts / len(cluster8_df)) * 100
    plt.pie(percentages.values, labels=[f"Sub-cluster {i}" for i in percentages.index], 
            autopct='%1.1f%%')
    plt.title("Sub-cluster Distribution (%)")
    
    # Word length distribution
    plt.subplot(2, 2, 3)
    word_lengths = cluster8_df["clean_joined"].str.split().str.len()
    plt.hist(word_lengths, bins=30, alpha=0.7)
    plt.title("Word Length Distribution")
    plt.xlabel("Number of Words")
    plt.ylabel("Frequency")
    
    # Character length distribution
    plt.subplot(2, 2, 4)
    char_lengths = cluster8_df["clean_joined"].str.len()
    plt.hist(char_lengths, bins=30, alpha=0.7)
    plt.title("Character Length Distribution")
    plt.xlabel("Number of Characters")
    plt.ylabel("Frequency")
    
    plt.tight_layout()
    plt.savefig("cluster8_subclustering_analysis.png", dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main function for sub-clustering cluster 8."""
    print("🔍 Cluster 8 Sub-clustering Analysis")
    print("=" * 50)
    
    try:
        # Load cluster 8 data
        cluster8_df = load_cluster8_data()
        
        # Build TF-IDF
        X, vec = build_tfidf_for_cluster8(cluster8_df)
        
        # Find optimal k
        best_k, scores = find_optimal_k(X, k_range=(2, 6))
        
        # Perform sub-clustering
        cluster8_df, kmeans = perform_sub_clustering(cluster8_df, X, vec, best_k)
        
        # Analyze sub-clusters
        analyze_sub_clusters(cluster8_df, vec, kmeans)
        
        # Save results
        output_path = save_sub_clustered_data(cluster8_df)
        
        # Create visualization
        create_visualization(cluster8_df)
        
        print(f"\n✅ Sub-clustering complete!")
        print(f"📁 Results saved to: {output_path}")
        print(f"📊 Visualization saved as: cluster8_subclustering_analysis.png")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 