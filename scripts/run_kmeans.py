#!/usr/bin/env python3
"""
K-Means Clustering Script
Applies K-means clustering to TF-IDF vectors with custom cluster numbers.
"""

import argparse
import pandas as pd
import numpy as np
from pathlib import Path
import sys
import time
import json
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns

def load_tfidf_data(tfidf_file: str, metadata_file: str = None):
    """
    Load TF-IDF vectors and metadata.
    
    Args:
        tfidf_file: Path to TF-IDF vectors CSV
        metadata_file: Path to metadata CSV (optional)
    
    Returns:
        X: TF-IDF matrix
        feature_names: List of feature names
        metadata: Metadata DataFrame (if provided)
    """
    print(f"📥 Loading TF-IDF vectors from {tfidf_file}...")
    
    # Load TF-IDF vectors
    tfidf_df = pd.read_csv(tfidf_file, index_col=0)
    print(f"✅ Loaded TF-IDF matrix: {tfidf_df.shape}")
    
    # Extract feature names and data
    feature_names = list(tfidf_df.columns)
    X = tfidf_df.values
    
    print(f"📊 Matrix shape: {X.shape}")
    print(f"🔤 Features: {len(feature_names)}")
    
    # Load metadata if provided
    metadata = None
    if metadata_file and Path(metadata_file).exists():
        print(f"📥 Loading metadata from {metadata_file}...")
        metadata = pd.read_csv(metadata_file)
        print(f"✅ Loaded metadata: {metadata.shape}")
    
    return X, feature_names, metadata

def run_kmeans(
    X: np.ndarray,
    n_clusters: int,
    random_state: int = 42,
    n_init: str = "auto",
    max_iter: int = 300
):
    """
    Run K-means clustering.
    
    Args:
        X: TF-IDF matrix
        n_clusters: Number of clusters
        random_state: Random seed
        n_init: Number of initializations
        max_iter: Maximum iterations
    
    Returns:
        kmeans: Fitted KMeans model
        labels: Cluster labels
        inertia: Model inertia
    """
    print(f"🔀 Running K-means with {n_clusters} clusters...")
    start_time = time.time()
    
    # Initialize and fit K-means
    kmeans = KMeans(
        n_clusters=n_clusters,
        random_state=random_state,
        n_init=n_init,
        max_iter=max_iter
    )
    
    labels = kmeans.fit_predict(X)
    inertia = kmeans.inertia_
    
    elapsed = time.time() - start_time
    print(f"✅ K-means completed in {elapsed:.2f}s")
    print(f"📊 Inertia: {inertia:.2f}")
    
    return kmeans, labels, inertia

def calculate_silhouette_score(X: np.ndarray, labels: np.ndarray, sample_size: int = 100000):
    """
    Calculate silhouette score with optional sampling.
    
    Args:
        X: TF-IDF matrix
        labels: Cluster labels
        sample_size: Sample size for calculation
    
    Returns:
        silhouette_score: Silhouette score
    """
    print(f"🎯 Calculating silhouette score...")
    
    if len(X) <= sample_size:
        score = silhouette_score(X, labels)
        print(f"✅ Silhouette score: {score:.4f}")
        return score
    
    # Sample data for faster calculation
    np.random.seed(42)
    indices = np.random.choice(len(X), sample_size, replace=False)
    X_sample = X[indices]
    labels_sample = labels[indices]
    
    score = silhouette_score(X_sample, labels_sample)
    print(f"✅ Silhouette score (sampled): {score:.4f}")
    return score

def analyze_clusters(labels: np.ndarray, metadata: pd.DataFrame = None):
    """
    Analyze cluster distribution and characteristics.
    
    Args:
        labels: Cluster labels
        metadata: Metadata DataFrame (optional)
    """
    print(f"\n📊 Cluster Analysis:")
    
    # Count cluster sizes
    unique_labels, counts = np.unique(labels, return_counts=True)
    
    print(f"📈 Cluster Distribution:")
    for label, count in zip(unique_labels, counts):
        percentage = (count / len(labels)) * 100
        print(f"  Cluster {label}: {count:,} ({percentage:.1f}%)")
    
    # Analyze metadata if available
    if metadata is not None:
        print(f"\n📋 Metadata Analysis:")
        
        # Add cluster labels to metadata
        metadata_with_clusters = metadata.copy()
        metadata_with_clusters["cluster"] = labels
        
        # Show sample records per cluster
        for cluster_id in sorted(unique_labels):
            cluster_data = metadata_with_clusters[metadata_with_clusters["cluster"] == cluster_id]
            print(f"\n  Cluster {cluster_id} sample records:")
            
            # Show first few records
            for i, (_, row) in enumerate(cluster_data.head(3).iterrows()):
                if "clean_joined" in row:
                    text = str(row["clean_joined"])[:100] + "..." if len(str(row["clean_joined"])) > 100 else str(row["clean_joined"])
                    print(f"    {i+1}. {text}")
                else:
                    print(f"    {i+1}. Record {row.get('doc_id', i)}")

def create_visualizations(
    labels: np.ndarray,
    output_dir: str,
    dataset_name: str = "clustering"
):
    """
    Create clustering visualizations.
    
    Args:
        labels: Cluster labels
        output_dir: Output directory
        dataset_name: Name for the dataset
    """
    print(f"📈 Creating visualizations...")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Cluster distribution bar chart
    plt.figure(figsize=(10, 6))
    unique_labels, counts = np.unique(labels, return_counts=True)
    
    plt.bar(unique_labels, counts, color='skyblue', edgecolor='navy')
    plt.title(f'Cluster Distribution - {dataset_name}')
    plt.xlabel('Cluster ID')
    plt.ylabel('Number of Documents')
    plt.xticks(unique_labels)
    
    # Add count labels on bars
    for i, count in enumerate(counts):
        plt.text(unique_labels[i], count + max(counts)*0.01, f'{count:,}', 
                ha='center', va='bottom', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path / f'{dataset_name}_cluster_distribution.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Cluster distribution pie chart
    plt.figure(figsize=(8, 8))
    plt.pie(counts, labels=[f'Cluster {label}' for label in unique_labels], 
            autopct='%1.1f%%', startangle=90)
    plt.title(f'Cluster Distribution - {dataset_name}')
    plt.axis('equal')
    plt.savefig(output_path / f'{dataset_name}_cluster_pie.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"📁 Visualizations saved to {output_path}")

def save_results(
    labels: np.ndarray,
    kmeans_model,
    metadata: pd.DataFrame,
    output_dir: str,
    dataset_name: str = "clustering"
):
    """
    Save clustering results.
    
    Args:
        labels: Cluster labels
        kmeans_model: Fitted KMeans model
        metadata: Metadata DataFrame
        output_dir: Output directory
        dataset_name: Name for the dataset
    """
    print(f"💾 Saving results...")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # 1. Save cluster labels
    results_df = pd.DataFrame({
        "doc_id": range(len(labels)),
        "cluster": labels
    })
    
    results_file = output_path / f"{dataset_name}_cluster_labels.csv"
    results_df.to_csv(results_file, index=False)
    print(f"📁 Cluster labels saved to: {results_file}")
    
    # 2. Save metadata with clusters
    if metadata is not None:
        metadata_with_clusters = metadata.copy()
        metadata_with_clusters["cluster"] = labels
        
        metadata_file = output_path / f"{dataset_name}_metadata_with_clusters.csv"
        metadata_with_clusters.to_csv(metadata_file, index=False)
        print(f"📁 Metadata with clusters saved to: {metadata_file}")
    
    # 3. Save model info
    model_info = {
        "n_clusters": kmeans_model.n_clusters,
        "inertia": float(kmeans_model.inertia_),
        "n_iter": kmeans_model.n_iter_,
        "cluster_centers_shape": kmeans_model.cluster_centers_.shape,
        "random_state": kmeans_model.random_state,
        "n_samples": len(labels)
    }
    
    model_file = output_path / f"{dataset_name}_model_info.json"
    with open(model_file, 'w') as f:
        json.dump(model_info, f, indent=2)
    print(f"📁 Model info saved to: {model_file}")
    
    # 4. Save cluster centers
    centers_df = pd.DataFrame(
        kmeans_model.cluster_centers_,
        columns=[f"feature_{i}" for i in range(kmeans_model.cluster_centers_.shape[1])]
    )
    centers_df.index = [f"cluster_{i}" for i in range(kmeans_model.n_clusters)]
    
    centers_file = output_path / f"{dataset_name}_cluster_centers.csv"
    centers_df.to_csv(centers_file)
    print(f"📁 Cluster centers saved to: {centers_file}")

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Run K-means clustering on TF-IDF vectors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic clustering with 5 clusters
  python scripts/run_kmeans.py --input data/processed/tfidf_vectors.csv --clusters 5
  
  # Clustering with metadata and custom output
  python scripts/run_kmeans.py --input tfidf_vectors.csv --metadata metadata.csv --clusters 8 --output results
  
  # Quick test with 3 clusters
  python scripts/run_kmeans.py --input tfidf_vectors.csv --clusters 3 --no-viz
        """
    )
    
    parser.add_argument(
        "--input", 
        required=True,
        help="Path to TF-IDF vectors CSV file"
    )
    
    parser.add_argument(
        "--metadata", 
        help="Path to metadata CSV file (optional)"
    )
    
    parser.add_argument(
        "--clusters", 
        type=int, 
        required=True,
        help="Number of clusters to create"
    )
    
    parser.add_argument(
        "--output", 
        default="clustering_results",
        help="Output directory (default: clustering_results)"
    )
    
    parser.add_argument(
        "--random-state", 
        type=int, 
        default=42,
        help="Random seed (default: 42)"
    )
    
    parser.add_argument(
        "--max-iter", 
        type=int, 
        default=300,
        help="Maximum iterations (default: 300)"
    )
    
    parser.add_argument(
        "--sample-size", 
        type=int, 
        default=100000,
        help="Sample size for silhouette calculation (default: 100000)"
    )
    
    parser.add_argument(
        "--no-viz", 
        action="store_true",
        help="Skip creating visualizations"
    )
    
    parser.add_argument(
        "--dataset-name", 
        default="clustering",
        help="Dataset name for output files (default: clustering)"
    )
    
    args = parser.parse_args()
    
    try:
        # Load data
        X, feature_names, metadata = load_tfidf_data(args.input, args.metadata)
        
        # Run K-means
        kmeans, labels, inertia = run_kmeans(
            X, 
            n_clusters=args.clusters,
            random_state=args.random_state,
            max_iter=args.max_iter
        )
        
        # Calculate silhouette score
        silhouette = calculate_silhouette_score(X, labels, args.sample_size)
        
        # Analyze clusters
        analyze_clusters(labels, metadata)
        
        # Create visualizations
        if not args.no_viz:
            create_visualizations(labels, args.output, args.dataset_name)
        
        # Save results
        save_results(labels, kmeans, metadata, args.output, args.dataset_name)
        
        # Summary
        print(f"\n🎉 Clustering completed successfully!")
        print(f"📊 Results:")
        print(f"  Clusters: {args.clusters}")
        print(f"  Documents: {len(labels):,}")
        print(f"  Features: {len(feature_names):,}")
        print(f"  Inertia: {inertia:.2f}")
        print(f"  Silhouette Score: {silhouette:.4f}")
        print(f"  Output Directory: {args.output}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 