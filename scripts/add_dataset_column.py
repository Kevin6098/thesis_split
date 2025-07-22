import pandas as pd

# File paths
high_rating_path = 'data/raw/high_rating_comments.csv'
most_commented_path = 'data/raw/most_commented_comments.csv'

# Output paths
high_rating_out = 'data/raw/high_rating_comments_with_dataset.csv'
most_commented_out = 'data/raw/most_commented_comments_with_dataset.csv'

# Add dataset column to high_rating
hr_df = pd.read_csv(high_rating_path)
hr_df['dataset'] = 'high_rating'
hr_df.to_csv(high_rating_out, index=False)

# Add dataset column to most_commented
mc_df = pd.read_csv(most_commented_path)
mc_df['dataset'] = 'most_commented'
mc_df.to_csv(most_commented_out, index=False)

print('Done: Added dataset column and saved new CSVs.') 