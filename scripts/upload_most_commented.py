#!/usr/bin/env python
import os
from pathlib import Path
import re

import psycopg2
from psycopg2.extras import execute_values
import pandas as pd
from dotenv import load_dotenv
from tqdm import tqdm

# ───────── Config ────────────────────────────────────────────
load_dotenv()
PG_CONN_STR = os.getenv("PG_CONN_STR")
if not PG_CONN_STR:
    raise RuntimeError("PG_CONN_STR env-var not set")

ROOT     = Path(__file__).resolve().parents[1]           # thesis_split/
CSV_PATH = ROOT / "data" / "raw" / "most_commented_comments_with_dataset.csv"
TARGET   = "public.most_commented_reviews"               # schema.table
CHUNK    = 5_000

DATE_COL = "date"
TS_COL   = "created_at"
# ─────────────────────────────────────────────────────────────

DATE_RE = re.compile(r"(\d{4})[/-](\d{2})(?:[/-](\d{2}))?")  # Y/M/[D]


def clean_date(df: pd.DataFrame, col: str = DATE_COL) -> pd.DataFrame:
    if col not in df.columns:
        return df

    def _extract(s: str) -> str | None:
        m = DATE_RE.search(str(s))
        if not m:
            return None
        y, mth, d = m.groups()
        d = d or "01"
        return f"{y}-{mth}-{d}"

    df[col] = pd.to_datetime(df[col].map(_extract), errors="coerce").dt.date
    return df


def clean_timestamp(df: pd.DataFrame, col: str = TS_COL) -> pd.DataFrame:
    if col in df.columns:
        df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def clean_id(df: pd.DataFrame, col: str = "id") -> pd.DataFrame:
    """
    Ensure id is BIGINT-compatible. Non-numeric → NaN → drop row.
    """
    if col not in df.columns:
        raise ValueError("CSV missing mandatory 'id' column")

    df[col] = pd.to_numeric(df[col], errors="coerce", downcast="integer")
    before = len(df)
    df = df[df[col].notna()]
    dropped = before - len(df)
    if dropped:
        print(f"⚠️  Dropped {dropped} rows with non-numeric id")
    return df


def df_to_rows(df: pd.DataFrame) -> list[list]:
    """
    Convert DataFrame chunk to list-of-lists; NaN/NaT/NA → None.
    """
    obj = df.astype(object).where(pd.notnull(df), None)
    return obj.values.tolist()


def main() -> None:
    # ── read & sanitise once ─────────────────────────────────
    df = pd.read_csv(CSV_PATH, low_memory=False)
    df = clean_id(df)          # <- NEW
    df = clean_date(df)
    df = clean_timestamp(df)

    # ── open connection ─────────────────────────────────────
    with psycopg2.connect(PG_CONN_STR) as conn, conn.cursor() as cur:
        schema, tbl = TARGET.split(".", 1)
        cur.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = %s AND table_name = %s
            """,
            (schema, tbl),
        )
        valid_cols = {r[0] for r in cur.fetchall()}
        df = df[[c for c in df.columns if c in valid_cols]]

        cols_sql = ",".join(f'"{c}"' for c in df.columns)
        total    = (len(df) + CHUNK - 1) // CHUNK

        with tqdm(total=total, desc="Uploading most_commented") as bar:
            for start in range(0, len(df), CHUNK):
                chunk = df.iloc[start:start + CHUNK]
                rows  = df_to_rows(chunk)

                execute_values(
                    cur,
                    f"""
                    INSERT INTO {TARGET} ({cols_sql}) VALUES %s
                    ON CONFLICT (id) DO NOTHING
                    """,
                    rows,
                    page_size=CHUNK,
                )
                bar.update()

        conn.commit()
        print(f"✓ Inserted / kept {len(df):,} rows in {TARGET}")


if __name__ == "__main__":
    main()