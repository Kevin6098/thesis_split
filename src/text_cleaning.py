# src/text_cleaning.py
# -------------------------------------
"""Cleansing & tokenisation of Japanese review text."""

from __future__ import annotations
import re, unicodedata
import pandas as pd
import numpy as np
from janome.tokenizer import Tokenizer
from tqdm import tqdm
from .stop_words import JP_STOPWORDS

# Patterns for noise removal
_RE_URL      = re.compile(r"https?://\S+")
_RE_EMAIL    = re.compile(r"\S+@\S+")
_RE_TAG      = re.compile(r"<[^>]+>")
_RE_HASHTAG  = re.compile(r"#[\w\u4E00-\u9FFF]+")

# Janome tokenizer (wakati mode)
_tokenizer = Tokenizer("-o wakati")

# Synonym mapping for unification
SYNONYM_MAP = {
    # ラーメン関連
    "中華そば": "ラーメン",
    "そば": "ラーメン",  # only in ラーメン context, but here applied globally
    # 寿司関連
    "寿司": "すし",
    "鮨": "すし",
    # 蕎麦関連
    "蕎麦": "そば",
    # 焼き関連
    "焼き加減": "焼き加減",  # Keep as compound
    # その他
    "食べログ": "ログ",
    # Add more as needed
}

# Compound words that should be preserved as bigrams
COMPOUND_WORDS = {
    "焼き鳥", "焼き加減", "焼肉", "予約困難", "待ち時間", 
    "コース料理", "ワインペアリング", "握り寿司", "刺身", "天ぷら",
    "焼き魚", "焼き肉", "焼き野菜", "焼き飯", "焼きそば"
}

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

def _improve_spacing_and_paragraphs(text: str) -> str:
    """Improve spacing and paragraph handling."""
    # Replace multiple newlines with single space
    text = re.sub(r'\n+', ' ', text)
    
    # Replace multiple spaces with single space
    text = re.sub(r'\s+', ' ', text)
    
    # Handle common paragraph separators
    text = re.sub(r'。\s*。', '。', text)  # Remove double periods
    text = re.sub(r'！\s*！', '！', text)  # Remove double exclamation marks
    text = re.sub(r'？\s*？', '？', text)  # Remove double question marks
    
    # Clean up spacing around punctuation
    text = re.sub(r'\s*([。、！？])\s*', r'\1', text)
    
    # Remove leading/trailing whitespace
    text = text.strip()
    
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

def _apply_synonym_map(tokens: list[str]) -> list[str]:
    """Replace tokens with their synonyms if present in the map."""
    return [SYNONYM_MAP.get(t, t) for t in tokens]

def _preserve_compounds(tokens: list[str]) -> list[str]:
    """Preserve compound words as bigrams when they appear together."""
    if len(tokens) < 2:
        return tokens
    
    preserved = []
    i = 0
    while i < len(tokens) - 1:
        bigram = tokens[i] + tokens[i + 1]
        if bigram in COMPOUND_WORDS:
            preserved.append(bigram)
            i += 2
        else:
            preserved.append(tokens[i])
            i += 1
    
    # Add the last token if we didn't skip it
    if i < len(tokens):
        preserved.append(tokens[i])
    
    return preserved

def _pos_ok(token: str) -> bool:
    """Keep only nouns (名詞) and important adjectives (形容詞), suppress generic evaluation words."""
    try:
        info = next(_tokenizer.tokenize(token))
    except StopIteration:
        return False
    pos = info.part_of_speech.split(",")[0]
    
    # Keep nouns and adjectives
    if pos in {"名詞", "形容詞"}:
        # Suppress generic evaluation adjectives
        generic_adj = {"良い", "いい", "感じ", "思う", "思った", "思います"}
        if token in generic_adj:
            return False
        return True
    
    return False

def _extra_ok(token: str) -> bool:
    """Drop single-char hiragana, 'し', and stopwords."""
    # Special handling for ない/なく - keep them if they're part of adjective forms
    if token in ["ない", "なく"]:
        return True  # Keep ない/なく, we'll handle merging in _merge_adj_negation
    
    return len(token) > 1 and token != "し" and token not in JP_STOPWORDS

def _merge_adj_negation(tokens: list[str]) -> list[str]:
    """Merge ない with preceding adjective forms."""
    merged = []
    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens) and tokens[i + 1] in ["ない", "なく"]:
            # Check if the previous token is an adjective form
            prev_token = tokens[i]
            # Handle various adjective endings that can be followed by ない/なく
            if (prev_token.endswith(("く", "しく", "らしく", "い", "しい", "らしい")) or 
                prev_token.endswith(("た", "かった", "らしかった"))):
                # Merge adjective + ない/なく
                merged.append(prev_token + tokens[i + 1])
                i += 2  # Skip both tokens
            else:
                merged.append(tokens[i])
                i += 1
        else:
            merged.append(tokens[i])
            i += 1
    return merged

def _merge_suffixes(tokens: list[str], suffixes=["ない", "たい"]) -> list[str]:
    """Merge any token with a following suffix (e.g., ない, たい)."""
    merged = []
    i = 0
    while i < len(tokens):
        if i + 1 < len(tokens) and tokens[i + 1] in suffixes:
            merged.append(tokens[i] + tokens[i + 1])
            i += 2
        else:
            merged.append(tokens[i])
            i += 1
    return merged

def _normalize_inflections(tokens: list[str]) -> list[str]:
    """Normalize common inflectional endings to standard forms."""
    normalized = []
    for t in tokens:
        # Handle common adjective/verb endings
        if t.endswith("かっ"):
            t = t.replace("かっ", "かった")
        elif t.endswith("なく"):
            t = t.replace("なく", "ない")
        elif t.endswith("く"):
            # Keep く as is for now, but could be normalized further if needed
            pass
        # Add more inflection rules as needed
        normalized.append(t)
    return normalized

def clean_comment(text: str) -> str:
    """Full pipeline for one comment → cleaned, space-joined tokens."""
    # Handle NaN values
    if pd.isna(text) or text == 'nan' or text == '' or str(text).strip() == '':
        return ""
    
    # Convert to string if not already
    text = str(text)
    
    text = _nfkc_lower(text)
    text = _strip_noise(text)
    text = _improve_spacing_and_paragraphs(text)
    text = _remove_noncontent(text)
    
    # Skip processing if text is empty after cleaning
    if not text.strip():
        return ""
    
    tokens = _tokenise(text)
    tokens = _apply_synonym_map(tokens)
    tokens = _preserve_compounds(tokens) # Apply compound word preservation
    tokens = _normalize_inflections(tokens)
    tokens = [t for t in tokens if _pos_ok(t) and _extra_ok(t)]
    # Merge suffixes (ない, たい)
    tokens = _merge_suffixes(tokens, suffixes=["ない", "たい"])
    return " ".join(tokens)

def cleanse_dataframe(df: pd.DataFrame, text_col: str = "comment") -> pd.DataFrame:
    """Apply `clean_comment` to every row, storing result in `clean_joined`."""
    df = df.copy()
    
    # Filter out rows with NaN or empty comments before processing
    print(f"📊 Original dataset size: {len(df):,}")
    
    # Check for NaN values in the text column
    nan_count = df[text_col].isna().sum()
    empty_count = (df[text_col].astype(str).str.strip() == '').sum()
    print(f"📊 Rows with NaN comments: {nan_count:,}")
    print(f"📊 Rows with empty comments: {empty_count:,}")
    
    # Create a mask for valid comments
    valid_mask = df[text_col].notna() & (df[text_col].astype(str).str.strip() != '')
    df_valid = df[valid_mask].copy()
    df_invalid = df[~valid_mask].copy()
    
    print(f"📊 Valid comments to process: {len(df_valid):,}")
    print(f"📊 Invalid comments (will be set to empty): {len(df_invalid):,}")
    
    # Add progress bar for text cleaning
    print("🔄 Cleaning text data...")
    cleaned_texts = []
    for text in tqdm(df_valid[text_col].astype(str), desc="Cleaning comments", unit="comment"):
        cleaned_texts.append(clean_comment(text))
    
    # Set cleaned text for valid comments
    df_valid["clean_joined"] = cleaned_texts
    
    # Set empty string for invalid comments
    df_invalid["clean_joined"] = ""
    
    # Combine the dataframes
    df_cleaned = pd.concat([df_valid, df_invalid], ignore_index=True)
    
    # Sort by original index to maintain order
    df_cleaned = df_cleaned.sort_index()
    
    # Final statistics
    non_empty_cleaned = (df_cleaned["clean_joined"] != "").sum()
    print(f"📊 Final non-empty cleaned comments: {non_empty_cleaned:,}")
    print(f"📊 Final empty cleaned comments: {len(df_cleaned) - non_empty_cleaned:,}")
    
    return df_cleaned