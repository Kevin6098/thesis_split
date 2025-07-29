import pandas as pd
from pathlib import Path

RAW_DIR = Path('data/raw')
OUT_DIR = Path('data/filtered')
OUT_DIR.mkdir(exist_ok=True)

# List of files to process
files = [
    'both_comments.csv',
    'most_commented_comments.csv',
    'high_rating_comments.csv',
]

for fname in files:
    in_path = RAW_DIR / fname
    out_path = OUT_DIR / fname
    print(f'Processing {in_path}...')
    # Read in chunks to handle large files
    chunks = []
    for chunk in pd.read_csv(in_path, chunksize=10000):
        # Drop rows where comment is missing
        chunk = chunk.dropna(subset=['comment'])
        # Keep only comments with <400 characters
        filtered = chunk[chunk['comment'].astype(str).apply(len) < 400]
        chunks.append(filtered)
    # Concatenate and save
    result = pd.concat(chunks, ignore_index=True)
    result.to_csv(out_path, index=False)
    print(f'Saved filtered file to {out_path} ({len(result)} rows)') 