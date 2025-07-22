#!/usr/bin/env python
"""
Bulk-loads both CSVs into public.all_reviews and tags each row
with dataset='high_rating' or 'most_commented'.
"""
import os, re, time
from pathlib import Path
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
from tqdm import tqdm
import warnings

# ─── Config ─────────────────────────────────────────────────
load_dotenv()
PG_CONN_STR = os.getenv("PG_CONN_STR")
if not PG_CONN_STR:
    raise RuntimeError("PG_CONN_STR env-var not set")

ROOT = Path(__file__).resolve().parents[1]
CSV_INPUTS = [
    ("high_rating",    ROOT / "data/raw/high_rating_comments_with_dataset.csv"),
    ("most_commented", ROOT / "data/raw/most_commented_comments_with_dataset.csv"),
]

TARGET  = "public.all_reviews"
CHUNK   = 800                             # keep each INSERT < 60 s
DATE_RE = re.compile(r"(\d{4})[/-](\d{2})(?:[/-](\d{2}))?")

# ─── Helpers ────────────────────────────────────────────────
warnings.filterwarnings("ignore", category=pd.errors.SettingWithCopyWarning)

def norm_date(s: str | None):
    if not isinstance(s, str):
        return None
    m = DATE_RE.search(s)
    if not m:
        return None
    y, mth, d = m.groups(); d = d or "01"
    return f"{y}-{mth}-{d}"

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df.loc[:, "id"] = pd.to_numeric(df["id"], errors="coerce", downcast="integer")
    df = df[df["id"].notna()]
    if "date" in df.columns:
        df.loc[:, "date"] = pd.to_datetime(
            df["date"].map(norm_date), errors="coerce"
        ).dt.date
    if "created_at" in df.columns:
        df.loc[:, "created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    return df

def to_rows(df: pd.DataFrame):
    return df.astype(object).where(pd.notnull(df), None).values.tolist()

# ─── Load ───────────────────────────────────────────────────
def main():
    with psycopg2.connect(PG_CONN_STR) as conn, conn.cursor() as cur:

        cur.execute("set statement_timeout = '55s'")

        cur.execute("""
            select column_name
            from information_schema.columns
            where table_schema = 'public' and table_name = 'all_reviews'
            order by ordinal_position
        """)
        cols = [r[0] for r in cur.fetchall()]
        cols_sql = ",".join(f'"{c}"' for c in cols)

        # drop index during bulk insert
        cur.execute("drop index if exists all_reviews_comment_trgm")
        conn.commit()

        for tag, csv_path in CSV_INPUTS:
            print(f"\n⇒ Loading {csv_path.name}  (dataset={tag})")
            df = pd.read_csv(csv_path, low_memory=False)
            df["dataset"] = tag
            df = clean(df)
            df = df[[c for c in cols if c in df.columns]]  # keep only valid cols

            total_batches = (len(df) + CHUNK - 1) // CHUNK
            with tqdm(total=total_batches, desc=f"Inserting {tag}") as bar:
                for start in range(0, len(df), CHUNK):
                    rows = to_rows(df.iloc[start : start + CHUNK])
                    execute_values(
                        cur,
                        f"""
                        insert into {TARGET} ({cols_sql}) values %s
                        on conflict (id) do update
                          set dataset = excluded.dataset
                        """,
                        rows,
                        page_size=CHUNK,
                    )
                    bar.update()
            conn.commit()
            print(f"✓ {len(df):,} rows inserted for {tag}")

    # ── create trigram index outside a tx ────────────────────
    print("Re-creating trigram index (concurrently)…")
    c2 = psycopg2.connect(PG_CONN_STR)
    c2.autocommit = True               # <- psycopg2 way (no kw arg)
    with c2.cursor() as cur2:
        cur2.execute("""
            create index concurrently if not exists all_reviews_comment_trgm
              on public.all_reviews using gin (comment gin_trgm_ops)
        """)
    c2.close()
    print("✓ Index ready")

if __name__ == "__main__":
    t0 = time.time()
    main()
    print(f"Total elapsed: {time.time() - t0:,.1f} s")