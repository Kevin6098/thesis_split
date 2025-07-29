#!/usr/bin/env python3
"""
Standalone Clustering Script
Runs the clustering stage independently from the main pipeline.
"""

import argparse
import pandas as pd
from pathlib import Path
import sys

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / "src"))

from config import DATA_DIR, MODEL_DIR, DATASETS
from vectorize import build_tfidf
from cluster_eval import fast_best_k_silhouette
from clustering import fit_kmeans

def run_clustering(slug: str, sample_size: int = 100000, k_min: int = 2, k_max: int = 9):
    """
    Run clustering stage for a specific dataset.
    
    Args:
        slug: Dataset name (high_rating or most_commented)
        sample_size: Sample size for silhouette calculation
        k_min: Minimum k value to test
        k_max: Maximum k value to test
    """
    print(f"🚀 Starting clustering for dataset: {slug}")
    print(f"🎲 Using sampling (sample_size={sample_size:,}) for faster computation")
    print(f"🔍 Testing k range: {k_min} to {k_max}")
    
    # Check if dataset exists
    if slug not in DATASETS:
        raise ValueError(f"Dataset '{slug}' not found. Available: {list(DATASETS.keys())}")
    
    # Load cleaned data
    clean_path = DATA_DIR / "processed" / f"{slug}_clean_text.parquet"
    if not clean_path.exists():
        raise FileNotFoundError(f"Cleaned data not found at {clean_path}. Run 'python main.py --set {slug} --stage clean' first.")
    
    print("📥 Loading cleaned data...")
    df = pd.read_parquet(clean_path)
    print(f"✅ Loaded {len(df):,} cleaned records")
    
    # Build TF-IDF vectors and get valid/invalid splits
    print("🔍 Building TF-IDF vectors...")
    X, vec, df_valid, df_invalid = build_tfidf(df)
    print(f"✅ TF-IDF built: {X.shape}")
    print(f"📊 Valid documents: {len(df_valid):,}")
    print(f"⚠️  Invalid documents: {len(df_invalid):,}")
    
    # Find optimal k using silhouette score
    print(f"🔎 Running silhouette score to find optimal k...")
    best_k, scores = fast_best_k_silhouette(
        X, 
        k_min=k_min, 
        k_max=k_max, 
        sample_size=min(sample_size, X.shape[0])
    )
    print(f"🎯 Optimal k: {best_k}")
    
    # Show silhouette scores for all tested k values
    print("\n📊 Silhouette Scores:")
    for k in sorted(scores.keys()):
        marker = "🎯" if k == best_k else "  "
        print(f"{marker} k={k}: {scores[k]:.4f}")
    
    # Fit K-means on valid documents only
    print(f"\n🔀 Fitting K-means with k={best_k}...")
    model_path = MODEL_DIR / f"{slug}_improved_kmeans.pkl"
    km = fit_kmeans(X, best_k, model_path)
    
    # Assign clusters
    df_valid["cluster"] = km.labels_
    df_invalid["cluster"] = -1  # Special label for invalid documents
    
    # Combine the dataframes
    df_with_clusters = pd.concat([df_valid, df_invalid], ignore_index=True)
    df_with_clusters = df_with_clusters.sort_index()  # Maintain original order
    
    # Save results
    out_path = DATA_DIR / "processed" / f"{slug}_improved_clustered.parquet"
    df_with_clusters.to_parquet(out_path, index=False)
    
    # Show cluster distribution
    cluster_counts = df_with_clusters["cluster"].value_counts().sort_index()
    print(f"\n📊 Cluster Distribution:")
    for cluster_id, count in cluster_counts.items():
        percentage = (count / len(df_with_clusters)) * 100
        if cluster_id == -1:
            print(f"  Invalid documents: {count:,} ({percentage:.1f}%)")
        else:
            print(f"  Cluster {cluster_id}: {count:,} ({percentage:.1f}%)")
    
    print(f"\n✅ Clustering completed successfully!")
    print(f"📁 Results saved to: {out_path}")
    print(f"🤖 Model saved to: {model_path}")
    
    return best_k, scores, out_path

def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(
        description="Run clustering analysis on a dataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic clustering with default settings
  python scripts/run_clustering.py --set high_rating
  
  # Custom k range and sample size
  python scripts/run_clustering.py --set most_commented --k-min 3 --k-max 12 --sample-size 50000
  
  # Quick test with smaller range
  python scripts/run_clustering.py --set high_rating --k-min 2 --k-max 6
        """
    )
    
    parser.add_argument(
        "--set", 
        choices=DATASETS.keys(), 
        required=True,
        help="Dataset to process (high_rating | most_commented)"
    )
    
    parser.add_argument(
        "--sample-size", 
        type=int, 
        default=100000,
        help="Sample size for silhouette calculation (default: 100000)"
    )
    
    parser.add_argument(
        "--k-min", 
        type=int, 
        default=2,
        help="Minimum k value to test (default: 2)"
    )
    
    parser.add_argument(
        "--k-max", 
        type=int, 
        default=9,
        help="Maximum k value to test (default: 9)"
    )
    
    args = parser.parse_args()
    
    try:
        best_k, scores, output_path = run_clustering(
            slug=args.set,
            sample_size=args.sample_size,
            k_min=args.k_min,
            k_max=args.k_max
        )
        
        print(f"\n🎉 Clustering analysis complete!")
        print(f"💡 Next steps:")
        print(f"   • Run topic analysis: python main.py --set {args.set} --stage topics")
        print(f"   • Generate visualizations: python main.py --set {args.set} --stage viz")
        print(f"   • Analyze specific cluster: python scripts/cluster_analysis_cluster8.py")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 