# src/text_cleaning.py
# -------------------------------------
"""Cleansing & tokenisation of Japanese review text."""

from __future__ import annotations
import re, unicodedata
import pandas as pd
from janome.tokenizer import Tokenizer
from .stop_words import JP_STOPWORDS

# Patterns for noise removal
_RE_URL      = re.compile(r"https?://\S+")
_RE_EMAIL    = re.compile(r"\S+@\S+")
_RE_TAG      = re.compile(r"<[^>]+>")
_RE_HASHTAG  = re.compile(r"#[\w\u4E00-\u9FFF]+")

# Janome tokenizer (wakati mode)
_tokenizer = Tokenizer("-o wakati")

def _nfkc_lower(text: str) -> str:
    """Normalize to NFKC and lowercase."""
    return unicodedata.normalize("NFKC", text).lower()

def _strip_noise(text: str) -> str:
    """Remove URLs, emails, hashtags, and HTML tags."""
    text = _RE_URL.sub(" ", text)
    text = _RE_EMAIL.sub(" ", text)
    text = _RE_HASHTAG.sub(" ", text)
    text = _RE_TAG.sub(" ", text)
    return text

def _remove_noncontent(text: str) -> str:
    """Remove digits (ascii & Japanese) and all other punctuation/symbols/emoji."""
    # 1) drop digits and Japanese numerals
    text = re.sub(r"[0-9０-９一二三四五六七八九〇十百千万億兆]+", " ", text)
    # 2) drop any char that is not:
    #    - word (Latin letters & underscore)
    #    - whitespace
    #    - Japanese (Hiragana, Katakana, CJK Unified)
    text = re.sub(r"[^\w\s\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FFF]", " ", text)
    return text

def _tokenise(text: str) -> list[str]:
    """Split into tokens (wakati)."""
    return list(_tokenizer.tokenize(text, wakati=True))

def _pos_ok(token: str) -> bool:
    """Keep only nouns (名詞) and adjectives (形容詞)."""
    try:
        info = next(_tokenizer.tokenize(token))
    except StopIteration:
        return False
    pos = info.part_of_speech.split(",")[0]
    return pos in {"名詞", "形容詞"}

def _extra_ok(token: str) -> bool:
    """Drop single-char hiragana, 'し', and stopwords."""
    return len(token) > 1 and token != "し" and token not in JP_STOPWORDS

def clean_comment(text: str) -> str:
    """Full pipeline for one comment → cleaned, space-joined tokens."""
    text = _nfkc_lower(text)
    text = _strip_noise(text)
    text = _remove_noncontent(text)
    tokens = _tokenise(text)
    tokens = [t for t in tokens if _pos_ok(t) and _extra_ok(t)]
    return " ".join(tokens)

def cleanse_dataframe(df: pd.DataFrame, text_col: str = "comment") -> pd.DataFrame:
    """Apply `clean_comment` to every row, storing result in `clean_joined`."""
    df = df.copy()
    df["clean_joined"] = df[text_col].astype(str).map(clean_comment)
    return df