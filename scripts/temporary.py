import pandas as pd
from pathlib import Path

csv_path = Path("/Users/kevinsoon/Documents/GitHub/thesis_split/data/raw/most_commented_comments_with_dataset.csv")  # adjust if needed
df = pd.read_csv(csv_path, nrows=0)   # read only the header
print(df.columns.tolist())