#!/usr/bin/env python3
"""
Cluster Analysis for Cluster 8
Analyzes the dominant cluster (cluster 8) from high rating data
"""

import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.feature_extraction.text import CountVectorizer

def load_clustered_data():
    """Load the clustered data and extract cluster 8."""
    data_path = Path("data/processed/high_rating_improved_clustered.parquet")
    if not data_path.exists():
        raise FileNotFoundError(f"Clustered data not found at {data_path}")
    
    df = pd.read_parquet(data_path)
    print(f"📊 Total records: {len(df):,}")
    
    # Get cluster distribution
    cluster_counts = df["cluster"].value_counts().sort_index()
    print(f"📊 Cluster distribution:")
    for cluster_id, count in cluster_counts.items():
        percentage = (count / len(df)) * 100
        print(f"  Cluster {cluster_id}: {count:,} ({percentage:.1f}%)")
    
    # Extract cluster 8
    cluster8_df = df[df["cluster"] == 8].copy()
    print(f"\n🎯 Cluster 8 analysis:")
    print(f"  Records in cluster 8: {len(cluster8_df):,}")
    print(f"  Percentage of total: {(len(cluster8_df) / len(df)) * 100:.1f}%")
    
    return df, cluster8_df

def analyze_cluster8_topics(cluster8_df, top_n=20):
    """Analyze the most common terms in cluster 8."""
    print(f"\n📝 Top {top_n} terms in Cluster 8:")
    
    # Combine all clean text
    all_text = " ".join(cluster8_df["clean_joined"].dropna().astype(str))
    
    # Count terms - fix min_df/max_df conflict
    vec = CountVectorizer(
        max_features=top_n,
        ngram_range=(1, 2),
        token_pattern=r"(?u)\b\w+\b",
        min_df=1,  # Changed from 5 to 1 to avoid conflict
        max_df=1.0  # Changed to 1.0 to avoid conflict
    )
    
    # Fit and get feature names
    vec.fit([all_text])
    feature_names = vec.get_feature_names_out()
    
    # Transform and get counts
    X = vec.transform([all_text])
    counts = X.toarray()[0]
    
    # Create sorted list of (term, count)
    term_counts = list(zip(feature_names, counts))
    term_counts.sort(key=lambda x: x[1], reverse=True)
    
    # Print results
    for i, (term, count) in enumerate(term_counts, 1):
        print(f"  {i:2d}. {term}: {count:,}")
    
    return term_counts

def analyze_cluster8_sentiment(cluster8_df):
    """Analyze sentiment patterns in cluster 8."""
    print(f"\n😊 Sentiment analysis for Cluster 8:")
    
    # Simple keyword-based sentiment
    positive_keywords = ["美味しい", "美味しかった", "良い", "いい", "満足", "おすすめ"]
    negative_keywords = ["高い", "残念", "不味い", "ひどい", "悪い"]
    
    positive_count = 0
    negative_count = 0
    
    for text in cluster8_df["clean_joined"].dropna():
        text = str(text).lower()
        if any(kw in text for kw in positive_keywords):
            positive_count += 1
        if any(kw in text for kw in negative_keywords):
            negative_count += 1
    
    total = len(cluster8_df)
    print(f"  Positive mentions: {positive_count:,} ({positive_count/total*100:.1f}%)")
    print(f"  Negative mentions: {negative_count:,} ({negative_count/total*100:.1f}%)")
    print(f"  Neutral: {total - positive_count - negative_count:,} ({(total - positive_count - negative_count)/total*100:.1f}%)")

def sample_cluster8_reviews(cluster8_df, n_samples=10):
    """Show sample reviews from cluster 8."""
    print(f"\n📄 Sample reviews from Cluster 8:")
    
    # Get random samples
    samples = cluster8_df.sample(n=min(n_samples, len(cluster8_df)), random_state=42)
    
    for i, (_, row) in enumerate(samples.iterrows(), 1):
        print(f"\n  Sample {i}:")
        print(f"    Original: {row['comment'][:200]}...")
        print(f"    Cleaned: {row['clean_joined'][:150]}...")

def plot_cluster8_distribution(df, cluster8_df):
    """Create visualization of cluster 8 dominance."""
    plt.figure(figsize=(12, 6))
    
    # Create subplot 1: Cluster distribution
    plt.subplot(1, 2, 1)
    cluster_counts = df["cluster"].value_counts().sort_index()
    colors = ['red' if i == 8 else 'lightblue' for i in cluster_counts.index]
    cluster_counts.plot(kind='bar', color=colors)
    plt.title("Cluster Distribution")
    plt.xlabel("Cluster ID")
    plt.ylabel("Number of Reviews")
    plt.xticks(rotation=45)
    
    # Create subplot 2: Pie chart of cluster 8 vs others
    plt.subplot(1, 2, 2)
    cluster8_count = len(cluster8_df)
    other_count = len(df) - cluster8_count
    plt.pie([cluster8_count, other_count], 
            labels=['Cluster 8', 'Other Clusters'],
            autopct='%1.1f%%',
            colors=['red', 'lightblue'])
    plt.title("Cluster 8 vs Others")
    
    plt.tight_layout()
    plt.savefig("cluster8_analysis.png", dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main analysis function."""
    print("🔍 Cluster 8 Analysis")
    print("=" * 50)
    
    try:
        # Load data
        df, cluster8_df = load_clustered_data()
        
        # Analyze topics
        term_counts = analyze_cluster8_topics(cluster8_df)
        
        # Analyze sentiment
        analyze_cluster8_sentiment(cluster8_df)
        
        # Show sample reviews
        sample_cluster8_reviews(cluster8_df)
        
        # Create visualization
        plot_cluster8_distribution(df, cluster8_df)
        
        print(f"\n✅ Analysis complete! Visualization saved as 'cluster8_analysis.png'")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 