# scripts/price_histogram.py
import re, argparse
from pathlib import Path
import pandas as pd, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_YEN_RE = re.compile(r"[¥¥￥]?\s*([\d,]+)")
def yen_to_int(s):
    m = _YEN_RE.search(str(s))
    return int(m.group(1).replace(",", "")) if m else None

def make_hist(slug):
    df = pd.read_parquet(Path("data/processed")/f"{slug}_clean_text.parquet",
                         columns=["price"])
    prices = df["price"].map(yen_to_int).dropna()
    plt.hist(prices, bins=30)
    plt.xlabel("Price (JPY)"); plt.ylabel("Count")
    plt.title(f"Price distribution – {slug}")
    out = Path("data/processed")/f"{slug}_price_hist.png"
    plt.savefig(out, dpi=300); plt.clf()
    print("✅ saved", out)

if __name__ == "__main__":
    for slug in ("high_rating", "most_commented"):
        make_hist(slug)