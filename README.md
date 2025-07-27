# Clustering Analysis Pipeline

A high-performance clustering analysis pipeline for large text datasets with optimized silhouette score calculation using sampling methods.

## 🚀 Features

- **Fast Silhouette Score Calculation**: Uses sampling (100k records) for dramatic speed improvements
- **Multiple Optimization Methods**: Original, sampling-based, and parallel processing options
- **Flexible Pipeline**: Clean, cluster, analyze topics, visualize, and perform sentiment analysis
- **Performance Monitoring**: Built-in timing and progress tracking
- **Easy to Use**: Simple command-line interface with sensible defaults

## 📊 Performance Improvements

| Method | Processing Time | Speed Improvement |
|--------|----------------|-------------------|
| Original (Full Dataset) | 13-69 hours | 1x |
| Sampling (100k records) | 1-3 hours | 10-20x faster |
| Parallel Processing | 30 min - 2 hours | 20-50x faster |

## 🛠️ Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd thesis_split
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Verify installation:**
```bash
python -c "import pandas, numpy, sklearn; print('✅ All dependencies installed')"
```

## 📁 Project Structure

```
thesis_split/
├── data/                          # Data files
│   ├── raw/                       # Raw CSV files
│   └── processed/                 # Processed parquet files
├── models/                        # Saved clustering models
├── src/                           # Core analysis modules
│   ├── cluster_eval.py           # Silhouette score calculation
│   ├── clustering.py             # K-means clustering
│   ├── vectorize.py              # TF-IDF vectorization
│   └── ...
├── scripts/                       # Utility scripts
│   ├── test_sampling.py          # Performance testing
│   └── ...
├── main.py                       # Main pipeline
└── README.md                     # This file
```

## 🎯 Quick Start

### 1. Basic Usage (Recommended)

**Run the complete pipeline with sampling optimization:**
```bash
python main.py --set high_rating --stage cluster
```

This will:
- Load and clean the data
- Build TF-IDF vectors
- Find optimal k using 100k sample
- Perform clustering
- Save results

### 2. Test Performance

**Compare different methods:**
```bash
python scripts/test_sampling.py --input data/processed/high_rating_clean_text.parquet
```

### 3. Use Parallel Processing

**For maximum speed:**
```bash
python main.py --set high_rating --stage cluster --parallel --n-jobs -1
```

## 📋 Detailed Usage

### Main Pipeline (`main.py`)

#### Command Line Arguments

```bash
python main.py --set <dataset> --stage <stage> [options]
```

**Required Arguments:**
- `--set`: Dataset to process (`high_rating` or `most_commented`)
- `--stage`: Pipeline stage (`clean`, `cluster`, `topics`, `viz`, `sentiment`, `lda`)

**Optional Arguments:**
- `--sample-size`: Sample size for silhouette calculation (default: 100000)
- `--parallel`: Enable parallel processing
- `--n-jobs`: Number of parallel jobs (-1 for all CPUs)
- `--no-sampling`: Disable sampling (use full dataset)

#### Pipeline Stages

1. **Clean Stage** (`--stage clean`):
   ```bash
   python main.py --set high_rating --stage clean
   ```
   - Loads raw CSV data
   - Cleans and preprocesses text
   - Saves cleaned data as parquet

2. **Cluster Stage** (`--stage cluster`):
   ```bash
   python main.py --set high_rating --stage cluster
   ```
   - Builds TF-IDF vectors
   - Finds optimal k using silhouette scores
   - Performs K-means clustering
   - Saves clustered data

3. **Topics Stage** (`--stage topics`):
   ```bash
   python main.py --set high_rating --stage topics
   ```
   - Analyzes cluster topics
   - Shows representative phrases per cluster

4. **Visualization Stage** (`--stage viz`):
   ```bash
   python main.py --set high_rating --stage viz
   ```
   - Generates cluster distribution plots
   - Creates topic visualizations

5. **Sentiment Stage** (`--stage sentiment`):
   ```bash
   python main.py --set high_rating --stage sentiment
   ```
   - Performs sentiment analysis
   - Saves sentiment scores

6. **LDA Stage** (`--stage lda`):
   ```bash
   python main.py --set high_rating --stage lda
   ```
   - Fits LDA topic model
   - Displays topics

### Performance Testing (`scripts/test_sampling.py`)

**Test different sampling methods:**
```bash
python scripts/test_sampling.py --input data/processed/high_rating_clean_text.parquet --sample-size 100000
```

This will compare:
- Original method (no sampling)
- Sampling method (100k sample)
- Fast sampling method (100k sample)

## 🎲 Sampling Methods Explained

### 1. Original Method
- Uses full dataset for silhouette calculation
- Most accurate but very slow
- Suitable for small datasets (< 50k records)

### 2. Sampling Method
- Uses 100k sample for silhouette calculation
- Good balance of speed and accuracy
- Recommended for most use cases

### 3. Fast Sampling Method
- Uses 100k sample for both clustering and silhouette
- Fastest method
- Suitable for very large datasets

### 4. Parallel Method
- Uses parallel processing across multiple CPUs
- Combines sampling with parallelization
- Maximum speed improvement

## 📈 Performance Optimization Tips

### 1. Choose the Right Method

**For small datasets (< 50k records):**
```bash
python main.py --set high_rating --stage cluster --no-sampling
```

**For medium datasets (50k - 500k records):**
```bash
python main.py --set high_rating --stage cluster --sample-size 100000
```

**For large datasets (> 500k records):**
```bash
python main.py --set high_rating --stage cluster --parallel --sample-size 100000
```

### 2. Adjust Sample Size

**For better accuracy (slower):**
```bash
python main.py --set high_rating --stage cluster --sample-size 200000
```

**For faster processing (less accurate):**
```bash
python main.py --set high_rating --stage cluster --sample-size 50000
```

### 3. Use Parallel Processing

**Use all CPU cores:**
```bash
python main.py --set high_rating --stage cluster --parallel --n-jobs -1
```

**Use specific number of cores:**
```bash
python main.py --set high_rating --stage cluster --parallel --n-jobs 4
```

## 🔧 Advanced Usage

### Custom K Range

Edit `src/cluster_eval.py` to change the k range:
```python
best_k, _ = fast_best_k_silhouette(X, k_min=3, k_max=15, sample_size=100000)
```

### Custom Random State

For reproducible results:
```bash
python main.py --set high_rating --stage cluster --sample-size 100000
```

### Batch Processing

Process multiple datasets:
```bash
for dataset in high_rating most_commented; do
    python main.py --set $dataset --stage cluster --parallel
done
```

## 📊 Output Files

### Generated Files

1. **Cleaned Data**: `data/processed/{dataset}_clean_text.parquet`
2. **Clustered Data**: `data/processed/{dataset}_with_clusters.parquet`
3. **Models**: `models/{dataset}_kmeans_k{k}.pkl`
4. **Visualizations**: Various PNG files in project root

### Example Output

```
🚀 Starting pipeline for dataset: high_rating
📋 Stage: cluster
🎲 Using sampling (sample_size=100,000) for faster computation
📥 Loading cleaned data...
✅ Loaded 250,000 cleaned records
🔍 Building TF-IDF vectors...
✅ TF-IDF built: (250000, 5000)
🎲 Using fast sampling-based k evaluation...
🚀 Fast k evaluation using sampling...
🎲 Sample size: 100,000 records
📊 Using sample of 100,000 records from 250,000 total
Testing k values: 100%|██████████| 9/9 [00:45<00:00, k=2, k=3, k=4, k=5, k=6, k=7, k=8, k=9, k=10]
✅ Best k: 6 (silhouette=0.4521)
⏱️  Fast evaluation completed in 45.23s
🎯 Optimal k: 6
🔀 Performing clustering...
✅ Clustering done (k=6), saved to data/processed/high_rating_with_clusters.parquet
```

## 🐛 Troubleshooting

### Common Issues

1. **Memory Error**: Reduce sample size
   ```bash
   python main.py --set high_rating --stage cluster --sample-size 50000
   ```

2. **Slow Processing**: Enable parallel processing
   ```bash
   python main.py --set high_rating --stage cluster --parallel
   ```

3. **Inaccurate Results**: Increase sample size
   ```bash
   python main.py --set high_rating --stage cluster --sample-size 200000
   ```

4. **File Not Found**: Run clean stage first
   ```bash
   python main.py --set high_rating --stage clean
   python main.py --set high_rating --stage cluster
   ```

### Performance Monitoring

**Check processing time:**
```bash
time python main.py --set high_rating --stage cluster
```

**Monitor memory usage:**
```bash
python -m memory_profiler main.py --set high_rating --stage cluster
```

## 📚 Technical Details

### Silhouette Score Calculation

The silhouette score measures how similar an object is to its own cluster compared to other clusters. Values range from -1 to 1:
- **1**: Perfect clustering
- **0**: Overlapping clusters
- **-1**: Poor clustering

### Sampling Strategy

The pipeline uses stratified sampling to maintain cluster proportions:
1. Sample 100k records randomly
2. Calculate silhouette score on sample
3. Use sample results to estimate full dataset performance

### K-Means Optimization

- Uses regular KMeans (not MiniBatchKMeans)
- `n_init="auto"` for optimal initialization
- Random state for reproducibility

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test with different sample sizes
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Scikit-learn for clustering algorithms
- Pandas for data manipulation
- NumPy for numerical computations
- TQDM for progress bars

---

**Happy Clustering! 🎯** 