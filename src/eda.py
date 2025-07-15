import matplotlib.pyplot as plt
import seaborn as sns

sns.set_context("talk")

def rating_vs_reviews(df):
    plt.figure(figsize=(8,6))
    sns.scatterplot(x="rating", y="n_reviews", data=df, alpha=0.4)
    plt.yscale("log")
    plt.title("Rating vs #Reviews (log)")
    plt.show()