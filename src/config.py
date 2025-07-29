from pathlib import Path

ROOT          = Path(__file__).resolve().parents[1]
DATA_DIR      = ROOT / "data"
MODEL_DIR     = ROOT / "models"

DATASETS = {
    "high_rating"    : DATA_DIR / "filtered" / "high_rating_comments.csv",
    "most_commented" : DATA_DIR / "filtered" / "most_commented_comments.csv",
}

RANDOM_STATE            = 42
HIGH_RATING_QUANTILE    = 0.9
HIGH_COMMENT_QUANTILE   = 0.9

DATA_DIR.mkdir(exist_ok=True)
MODEL_DIR.mkdir(exist_ok=True)