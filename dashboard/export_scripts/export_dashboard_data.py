#!/usr/bin/env python
"""
Export all data needed for the React dashboard.
This script processes the analysis results and exports them as JSON files
for the dashboard to consume.

Usage:
    python dashboard/export_scripts/export_dashboard_data.py
"""

import json
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.metrics import silhouette_score
from joblib import load
import sys

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent.parent))

from src.config import DATA_DIR, MODEL_DIR
from src.vectorize import build_tfidf
from src.topic_inspection import extract_ngrams

def export_silhouette_analysis(slug: str, output_dir: Path):
    """Export silhouette scores for different k values."""
    try:
        # Load processed data
        clean_path = DATA_DIR / "processed" / f"{slug}_clean_text.parquet"
        if not clean_path.exists():
            print(f"Warning: {clean_path} not found, using mock data")
            # Generate mock silhouette data
            mock_data = []
            for k in range(2, 13):
                score = 0.4 + 0.1 * np.sin(k) + np.random.normal(0, 0.02)
                mock_data.append({"k": k, "silhouette": round(score, 3)})
            
            output_file = output_dir / f"{slug}_silhouette.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(mock_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Exported mock silhouette data: {output_file}")
            return
            
        df = pd.read_parquet(clean_path)
        X, _ = build_tfidf(df)
        
        silhouette_data = []
        for k in range(2, 13):
            try:
                model_path = MODEL_DIR / f"{slug}_kmeans_k{k}.pkl"
                if model_path.exists():
                    km = load(model_path)
                    score = silhouette_score(X, km.labels_)
                    silhouette_data.append({"k": k, "silhouette": round(score, 3)})
            except Exception as e:
                print(f"Warning: Could not load model for k={k}: {e}")
        
        if not silhouette_data:
            print(f"No silhouette data found, using mock data for {slug}")
            return export_silhouette_analysis(slug, output_dir)
            
        output_file = output_dir / f"{slug}_silhouette.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(silhouette_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Exported silhouette analysis: {output_file}")
        
    except Exception as e:
        print(f"Error exporting silhouette analysis for {slug}: {e}")

def export_cluster_distribution(slug: str, output_dir: Path):
    """Export cluster distribution data."""
    try:
        clustered_path = DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        if not clustered_path.exists():
            print(f"Warning: {clustered_path} not found, using mock data")
            # Generate mock cluster distribution
            np.random.seed(42)
            clusters = list(range(8 if slug == 'high_rating' else 9))
            counts = np.random.randint(100, 300, len(clusters))
            total = sum(counts)
            
            mock_data = []
            for i, (cluster, count) in enumerate(zip(clusters, counts)):
                percentage = round((count / total) * 100, 1)
                mock_data.append({
                    "cluster": cluster,
                    "count": int(count),
                    "percentage": percentage
                })
            
            output_file = output_dir / f"{slug}_cluster_distribution.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(mock_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Exported mock cluster distribution: {output_file}")
            return
        
        df = pd.read_parquet(clustered_path)
        cluster_counts = df['cluster'].value_counts().sort_index()
        total = len(df)
        
        distribution_data = []
        for cluster, count in cluster_counts.items():
            percentage = round((count / total) * 100, 1)
            distribution_data.append({
                "cluster": int(cluster),
                "count": int(count),
                "percentage": percentage
            })
        
        output_file = output_dir / f"{slug}_cluster_distribution.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(distribution_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Exported cluster distribution: {output_file}")
        
    except Exception as e:
        print(f"Error exporting cluster distribution for {slug}: {e}")

def export_lda_topics(slug: str, output_dir: Path):
    """Export LDA topic data."""
    try:
        lda_path = MODEL_DIR / f"{slug}_lda.pkl"
        if not lda_path.exists():
            print(f"Warning: {lda_path} not found, using mock data")
            # Generate mock LDA topics
            mock_topics = [
                {
                    "topic": 0,
                    "prevalence": 9.8,
                    "words": ["料理", "美味しい", "サービス", "雰囲気", "満足"],
                    "description": "Food Quality & Service"
                },
                {
                    "topic": 1,
                    "prevalence": 20.7,
                    "words": ["寿司", "新鮮", "大将", "技術", "職人"],
                    "description": "Sushi & Craftsmanship"
                }
                # Add more mock topics as needed
            ]
            
            output_file = output_dir / f"{slug}_lda_topics.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(mock_topics, f, indent=2, ensure_ascii=False)
            print(f"✅ Exported mock LDA topics: {output_file}")
            return
        
        lda, vec = load(lda_path)
        
        # Get topic prevalence from document-topic distributions
        clustered_path = DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        if clustered_path.exists():
            df = pd.read_parquet(clustered_path)
            X = vec.transform(df["clean_joined"].values)
            topic_dist = lda.transform(X)
            topic_prevalence = topic_dist.mean(axis=0) * 100
        else:
            # Use uniform distribution if no data
            topic_prevalence = [100 / lda.n_components] * lda.n_components
        
        # Get top words for each topic
        feature_names = vec.get_feature_names_out()
        topics_data = []
        
        for topic_id, (topic_weights, prevalence) in enumerate(zip(lda.components_, topic_prevalence)):
            top_word_indices = topic_weights.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_word_indices]
            
            topics_data.append({
                "topic": topic_id,
                "prevalence": round(prevalence, 1),
                "words": top_words,
                "description": f"Topic {topic_id}"
            })
        
        output_file = output_dir / f"{slug}_lda_topics.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(topics_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Exported LDA topics: {output_file}")
        
    except Exception as e:
        print(f"Error exporting LDA topics for {slug}: {e}")

def export_sentiment_analysis(slug: str, output_dir: Path):
    """Export sentiment analysis data."""
    try:
        sentiment_path = DATA_DIR / "processed" / f"{slug}_sentiment.parquet"
        if not sentiment_path.exists():
            print(f"Warning: {sentiment_path} not found, using mock data")
            # Generate mock sentiment data
            np.random.seed(42)
            if slug == 'high_rating':
                overall = {"positive": 0.78, "negative": 0.22}
                clusters = list(range(8))
            else:
                overall = {"positive": 0.62, "negative": 0.38}
                clusters = list(range(9))
            
            by_cluster = []
            for cluster in clusters:
                pos_ratio = np.random.uniform(0.4, 0.9)
                by_cluster.append({
                    "cluster": cluster,
                    "positive": round(pos_ratio, 2),
                    "negative": round(1 - pos_ratio, 2)
                })
            
            sentiment_data = {
                "overall": overall,
                "byCluster": by_cluster
            }
            
            output_file = output_dir / f"{slug}_sentiment.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(sentiment_data, f, indent=2, ensure_ascii=False)
            print(f"✅ Exported mock sentiment data: {output_file}")
            return
        
        df = pd.read_parquet(sentiment_path)
        
        # Overall sentiment distribution
        overall_sentiment = df['sentiment_label'].value_counts(normalize=True)
        overall = {
            "positive": round(overall_sentiment.get('positive', 0), 2),
            "negative": round(overall_sentiment.get('negative', 0), 2)
        }
        
        # Sentiment by cluster
        by_cluster = []
        for cluster in sorted(df['cluster'].unique()):
            cluster_df = df[df['cluster'] == cluster]
            cluster_sentiment = cluster_df['sentiment_label'].value_counts(normalize=True)
            by_cluster.append({
                "cluster": int(cluster),
                "positive": round(cluster_sentiment.get('positive', 0), 2),
                "negative": round(cluster_sentiment.get('negative', 0), 2)
            })
        
        sentiment_data = {
            "overall": overall,
            "byCluster": by_cluster
        }
        
        output_file = output_dir / f"{slug}_sentiment.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(sentiment_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Exported sentiment analysis: {output_file}")
        
    except Exception as e:
        print(f"Error exporting sentiment analysis for {slug}: {e}")

def export_representative_quotes(slug: str, output_dir: Path):
    """Export representative quotes for each cluster."""
    try:
        clustered_path = DATA_DIR / "processed" / f"{slug}_with_clusters.parquet"
        if not clustered_path.exists():
            print(f"Warning: {clustered_path} not found, using mock data")
            # Use quotes from representative_quotes.txt if available
            quotes_path = Path("representative_quotes.txt")
            if quotes_path.exists():
                # Parse the existing quotes file
                with open(quotes_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                mock_quotes = {}
                current_cluster = None
                for line in content.split('\n'):
                    if line.startswith('■ Cluster'):
                        cluster_num = int(line.split()[1])
                        current_cluster = cluster_num
                        mock_quotes[current_cluster] = []
                    elif line.startswith('・') and current_cluster is not None:
                        quote_text = line[2:].strip()
                        if quote_text and len(quote_text) > 10:
                            mock_quotes[current_cluster].append({
                                "comment": quote_text,
                                "sentiment": "positive",
                                "sentiment_score": 0.1,
                                "topic": current_cluster % 8
                            })
            else:
                mock_quotes = {0: [{"comment": "Mock quote", "sentiment": "positive", "sentiment_score": 0.1, "topic": 0}]}
            
            output_file = output_dir / f"{slug}_quotes.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(mock_quotes, f, indent=2, ensure_ascii=False)
            print(f"✅ Exported mock representative quotes: {output_file}")
            return
        
        df = pd.read_parquet(clustered_path)
        quotes_data = {}
        
        for cluster in sorted(df['cluster'].unique()):
            cluster_df = df[df['cluster'] == cluster]
            # Sample representative quotes
            sample_quotes = cluster_df.sample(min(3, len(cluster_df)))
            
            quotes_data[int(cluster)] = []
            for _, row in sample_quotes.iterrows():
                quotes_data[int(cluster)].append({
                    "comment": row['comment'][:200] + "..." if len(row['comment']) > 200 else row['comment'],
                    "sentiment": row.get('sentiment_label', 'positive'),
                    "sentiment_score": float(row.get('sentiment_score', 0.1)),
                    "topic": int(cluster) % 8  # Assume topic mapping
                })
        
        output_file = output_dir / f"{slug}_quotes.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(quotes_data, f, indent=2, ensure_ascii=False)
        print(f"✅ Exported representative quotes: {output_file}")
        
    except Exception as e:
        print(f"Error exporting representative quotes for {slug}: {e}")

def main():
    """Export all dashboard data."""
    print("🚀 Starting dashboard data export...")
    
    # Create output directory
    output_dir = Path("dashboard/public/data")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    datasets = ["high_rating", "most_commented"]
    
    for slug in datasets:
        print(f"\n📊 Processing {slug} dataset...")
        
        export_silhouette_analysis(slug, output_dir)
        export_cluster_distribution(slug, output_dir)
        export_lda_topics(slug, output_dir)
        export_sentiment_analysis(slug, output_dir)
        export_representative_quotes(slug, output_dir)
    
    print(f"\n✅ All data exported to {output_dir}")
    print("\n🎯 Next steps:")
    print("1. cd dashboard")
    print("2. npm install")
    print("3. npm run dev")

if __name__ == "__main__":
    main()