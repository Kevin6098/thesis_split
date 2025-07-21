"""
Script: analysis_summary.py
Summarise LDA & K-means findings for both corpora, save CSV & chart.
Usage: python src/analysis_summary.py
"""
import matplotlib
matplotlib.use("Agg")  
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

# Directories
proc_dir  = Path("data/processed")
model_dir = Path("models")

# Topic themes mapping
topic_map = {
    0: "Cuisine & Prestige",
    1: "Desire & Evaluation",
    2: "Dessert & Comparisons",
    3: "Queue & Wait Times",
    4: "Awards & Hype",
    5: "Reservation Frustration",
    6: "Ambiance & Location",
    7: "Menu Variety (Sushi)"
}

# Helper: compute prevalence
def get_prevalence(slug):
    df = pd.read_parquet(proc_dir / f"{slug}_with_clusters.parquet")
    lda, vec = joblib.load(model_dir / f"{slug}_lda.pkl")
    X = vec.transform(df["clean_joined"].values)
    topics = lda.transform(X).argmax(axis=1)
    return pd.Series(topics).value_counts(normalize=True).sort_index() * 100

# Compute for both
prev_hr = get_prevalence("high_rating")
prev_mc = get_prevalence("most_commented")

data = []
for t in sorted(topic_map):
    hr = prev_hr.get(t, 0.0)
    mc = prev_mc.get(t, 0.0)
    data.append({
        "Topic ID": t,
        "Theme": topic_map[t],
        "HighRating (%)": round(hr,1),
        "MostCommented (%)": round(mc,1),
        "Delta (%)": round(hr - mc,1)
    })
summary = pd.DataFrame(data)
# Save CSV
target_csv = proc_dir / "topic_summary.csv"
summary.to_csv(target_csv, index=False)
print(f"Saved summary table to {target_csv}")

# Print markdown to console
print("\nMarkdown Table:\n")
print(summary.to_markdown(index=False))

# Bar chart of Delta
plt.figure(figsize=(8,5))
colors = ['#2ca02c' if d>0 else '#d62728' for d in summary['Delta (%)']]
plt.barh(summary['Theme'], summary['Delta (%)'], color=colors)
plt.axvline(0, color='black', linewidth=0.8)
plt.title('High-Rating vs Most-Commented Delta by Topic')
plt.xlabel('Delta (%)')
plt.tight_layout()

img_path = proc_dir / 'delta_chart.png'
plt.savefig(img_path)
print(f"Saved delta chart to {img_path}")
plt.close()
