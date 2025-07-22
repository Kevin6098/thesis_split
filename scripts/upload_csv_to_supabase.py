import os
from pathlib import Path
import re

import psycopg2
import pandas as pd
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from tqdm import tqdm

# ──────────────────────── Config ─────────────────────────────
load_dotenv()
PG_CONN_STR = os.getenv("PG_CONN_STR")
if not PG_CONN_STR:
    raise RuntimeError("PG_CONN_STR env-var not set")

ROOT = Path(__file__).resolve().parents[1]  # thesis_split/

DATASETS = {
    ROOT / "data" / "raw" / "high_rating_comments_with_dataset.csv":  "public.high_rating_reviews",
    ROOT / "data" / "raw" / "most_commented_comments_with_dataset.csv": "public.most_commented_reviews",
}

CHUNK_SIZE = 5_000
DATE_COL = "date"
TS_COL   = "created_at"
# ──────────────────────────────────────────────────────────────


def chunk_iter(df: pd.DataFrame, size: int):
    for start in range(0, len(df), size):
        yield df.iloc[start:start + size]


# ────────────────  Date / Timestamp cleaners  ────────────────
DATE_RE = re.compile(r"(\d{4})[/-](\d{2})(?:[/-](\d{2}))?")

def fix_date_col(df: pd.DataFrame, col: str = DATE_COL) -> pd.DataFrame:
    if col not in df.columns:
        return df

    def _extract_date(s: str) -> str | None:
        m = DATE_RE.search(str(s))
        if not m:
            return None
        y, mth, d = m.groups()
        d = d or "01"          # default day
        return f"{y}-{mth}-{d}"

    cleaned = df[col].map(_extract_date)
    df[col] = pd.to_datetime(cleaned, errors="coerce").dt.date
    return df


def fix_timestamp_col(df: pd.DataFrame, col: str = TS_COL) -> pd.DataFrame:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")    # NaT on failure
    return df
# ──────────────────────────────────────────────────────────────


def to_sql_rows(df: pd.DataFrame) -> list[list]:
    """
    Convert DataFrame to list-of-lists with all NaN/NaT/NA → None.
    Keeps numeric types as Python scalars and dates/timestamps as is.
    """
    # Ensure object dtype so lambda sees the real Python objects
    df_obj = df.astype(object)
    return (
        df_obj.applymap(lambda x: None if pd.isna(x) else x)
              .values
              .tolist()
    )


def copy_dataframe(conn, df: pd.DataFrame, full_table_name: str):
    schema, table = full_table_name.split(".", 1) if "." in full_table_name else ("public", full_table_name)

    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            """,
            (schema, table),
        )
        valid_cols = {row[0] for row in cur.fetchall()}

    df = df[[c for c in df.columns if c in valid_cols]]
    if df.empty:
        print(f"⚠️  No matching columns to insert into {full_table_name}")
        return

    cols_sql = ",".join(f'"{c}"' for c in df.columns)
    total_batches = (len(df) + CHUNK_SIZE - 1) // CHUNK_SIZE

    with conn.cursor() as cur, tqdm(total=total_batches,
                                    desc=f"Inserting into {full_table_name}") as bar:
        for chunk in chunk_iter(df, CHUNK_SIZE):
            rows = to_sql_rows(chunk)                         # ← converts NaT→None
            execute_values(
                cur,
                f"INSERT INTO {full_table_name} ({cols_sql}) VALUES %s",
                rows,
                page_size=CHUNK_SIZE,
            )
            bar.update()
        conn.commit()


def main():
    with psycopg2.connect(PG_CONN_STR) as conn:
        for csv_path, table in DATASETS.items():
            df = pd.read_csv(csv_path, low_memory=False)
            df = fix_date_col(df, DATE_COL)
            df = fix_timestamp_col(df, TS_COL)
            copy_dataframe(conn, df, table)
            print(f"✓ Loaded {len(df):,} rows from {csv_path.name} into {table}")


if __name__ == "__main__":
    main()