import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from joblib import dump

CATS = ["prefecture", "genre", "station"]
NUMS = ["dinner_price", "lunch_price", "rating", "n_reviews"]

def train_quadrant_classifier(df: pd.DataFrame, model_path):
    X = df[CATS + NUMS]
    y = df["segment"]

    Xtr, Xte, ytr, yte = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    pipe = Pipeline([
        ("prep", ColumnTransformer([
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATS),
            ("num", "passthrough", NUMS),
        ])),
        ("rf",  RandomForestClassifier(n_estimators=400, random_state=42)),
    ])

    pipe.fit(Xtr, ytr)
    print(classification_report(yte, pipe.predict(Xte)))
    dump(pipe, model_path)
    return pipe