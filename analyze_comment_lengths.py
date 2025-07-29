import pandas as pd

# Load the sample CSV
csv_path = "data/processed/high_rating_sample_1000.csv"
df = pd.read_csv(csv_path)

# Drop rows with missing comments
comments = df['comment'].dropna().astype(str)

# Calculate lengths
char_lengths = comments.apply(len)
word_lengths = comments.apply(lambda x: len(x.split()))

# Print averages
print(f"Average characters per comment: {char_lengths.mean():.2f}")
print(f"Average words per comment: {word_lengths.mean():.2f}")
print(f"Total comments analyzed: {len(comments)}") 