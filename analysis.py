"""
main.py  –  Cluster & complaint analysis with disk-level caching
Run it as:  python main.py
"""

import os, pickle, json, joblib, unicodedata, re, regex, itertools, time
import pandas as pd
from collections import Counter
from janome.tokenizer import Tokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition      import TruncatedSVD
from sklearn.cluster            import MiniBatchKMeans
from sklearn.metrics            import silhouette_score

# ---------- configurable paths ----------
DATA_DIR   = "data"
CACHE_DIR  = "cache"
CSV_PATH   = os.path.join(DATA_DIR, "most_commented_comments.csv")
STOP_PY    = os.path.join(DATA_DIR, "stop_words.py")
TEXT_COL   = "comment"  # <-- Added: column name for text

os.makedirs(CACHE_DIR, exist_ok=True)

# ---------- tiny helper ----------
def cache_path(name): return os.path.join(CACHE_DIR, name)

# -------------------------------------------------
# 1) LOAD CSV   **FIXED**
# -------------------------------------------------
parquet_file = cache_path("comments.parquet")

if os.path.exists(parquet_file):
    df = pd.read_parquet(parquet_file)
    print("✅  loaded cached parquet")
else:
    # -- NEW: read every column as string to avoid mixed-dtype grief
    df = pd.read_csv(CSV_PATH, dtype=str, low_memory=False)
    
    # OR: if you care about certain numeric columns, do this instead:
    # df = pd.read_csv(CSV_PATH, low_memory=False)
    # for col in df.select_dtypes(["object"]).columns:
    #     df[col] = df[col].astype("string")
    
    df.to_parquet(parquet_file, index=False)
    print("🆕  csv → parquet saved (all cols = string)")

# ---------------------------------------------------------------
# 2)  CLEAN & TOKENISE  (nouns+adjectives, drop し/numbers/symbols/emoji)
# ---------------------------------------------------------------
tok_cache = cache_path("tokenised.pkl")

if os.path.exists(tok_cache):
    with open(tok_cache, "rb") as f:
        tokens_list = pickle.load(f)
    print("✅  token list loaded")
else:
    from janome.tokenizer import Tokenizer
    tkn = Tokenizer()

    KEEP_POS     = {"名詞", "形容詞"}
    HIRAGANA_1   = regex.compile(r"^\p{Hiragana}$")
    RE_DIGIT     = regex.compile(r"^[\d０-９]+$")
    KANJI_NUM    = set("一二三四五六七八九十百千万億兆")

    # ---------- load stop-words ----------
    from importlib import util as _iu
    spec = _iu.spec_from_file_location("sw", STOP_PY)
    if spec is None or spec.loader is None:
        raise ImportError(f"Could not load stop words from {STOP_PY}")
    sw = _iu.module_from_spec(spec)
    spec.loader.exec_module(sw)
    ALL_STOPS = set(sw.STOP_WORDS).union({"し"})

    # ---------- ⚙️ NEW: regexes to scrub symbols & emoji ----------
    SYMBOL_PAT = regex.compile(r"[\p{P}\p{S}]")               # all punct & symbols
    EMOJI_PAT  = regex.compile(r"\p{Extended_Pictographic}")  # full emoji range
    # -------------------------------------------------------------

    def is_kanji_num(s): return s and all(ch in KANJI_NUM for ch in s)

    def clean(text: str) -> str:
        if pd.isna(text): return ""
        text = unicodedata.normalize("NFKC", str(text))
        text = SYMBOL_PAT.sub(" ", text)      # ⚙️ remove punct/symbols
        text = EMOJI_PAT.sub(" ", text)       # ⚙️ remove emoji
        return re.sub(r"\s+", " ", text).strip()

    def tokens(text):
        out=[]
        for tk in tkn.tokenize(text):
            if tk.part_of_speech.split(',')[0] not in KEEP_POS: continue
            s=tk.surface
            if HIRAGANA_1.match(s) or s in ALL_STOPS: continue
            if RE_DIGIT.match(s)  or is_kanji_num(s): continue
            out.append(s)
        return out

    df["clean"]  = df[TEXT_COL].apply(clean)
    tokens_list  = df["clean"].apply(tokens).tolist()
    with open(tok_cache, "wb") as f:
        pickle.dump(tokens_list, f)
    print("🆕  tokenised & cached")
# join tokens for vectoriser
joined = [" ".join(toks) for toks in tokens_list]

# ------------------------------------------------------------------
# 3) TF-IDF + SVD   (saved as joblib)
# ------------------------------------------------------------------
vec_cache = cache_path("tfidf_svd.joblib")

if os.path.exists(vec_cache):
    tfidf, svd, X_small = joblib.load(vec_cache)
    print("✅  vector space loaded")
else:
    tfidf = TfidfVectorizer(
        tokenizer=str.split,
        preprocessor=None,
        max_df=0.7,
        min_df=5,
    )
    X = tfidf.fit_transform(joined)
    print("TF-IDF type:", type(X))

    # dimensionality reduction (100 dims)
    svd = TruncatedSVD(100, random_state=42)
    X_small = svd.fit_transform(X)
    joblib.dump((tfidf, svd, X_small), vec_cache)
    print("🆕  tfidf & svd cached")

# ------------------------------------------------------------------
# 4) SILHOUETTE SEARCH  (cached json with best k & scores)
# ------------------------------------------------------------------
sil_cache = cache_path("silhouette.json")

if os.path.exists(sil_cache):
    with open(sil_cache) as f:
        sil_data = json.load(f)
    best_k = sil_data["best_k"]
    print("✅  best k cached =", best_k)
else:
    scores = {}
    for k in range(2,11):
        mbk = MiniBatchKMeans(k, random_state=42,
                              batch_size=2048, n_init=str(5), max_iter=100)
        lbl = mbk.fit_predict(X_small)
        s   = silhouette_score(X_small, lbl,
                               sample_size=min(8000, len(lbl)),
                               random_state=42)
        scores[k]=round(s,4)
        print(f"k={k:<2}  sil={s:.4f}")

    best_k = max(list(scores.keys()), key=lambda k: scores[k])
    with open(sil_cache,"w") as f:
        json.dump({"scores":scores,"best_k":best_k}, f, indent=2)
    print("🆕  silhouette cached, best k =", best_k)

# ------------------------------------------------------------------
# 5) FINAL CLUSTERING  (cached)
# ------------------------------------------------------------------
clust_cache = cache_path(f"kmeans_k{best_k}.joblib")

if os.path.exists(clust_cache):
    mbk = joblib.load(clust_cache)
    print("✅  k-means model loaded")
else:
    mbk = MiniBatchKMeans(best_k, random_state=42,
                          batch_size=2048, n_init=str(10), max_iter=200)
    mbk.fit(X_small)
    joblib.dump(mbk, clust_cache)
    print("🆕  k-means saved")

labels = mbk.labels_
df["cluster"] = labels

# optional quick peek
term_names = tfidf.get_feature_names_out()
import numpy as np
if hasattr(mbk, 'cluster_centers_') and isinstance(mbk.cluster_centers_, np.ndarray):
    centroids = mbk.cluster_centers_.argsort()[:, ::-1]
    for c in range(best_k):
        idxs = centroids[c][:10]
        # Flatten idxs if it contains arrays
        flat_idxs = []
        for i in idxs:
            if isinstance(i, np.ndarray):
                flat_idxs.extend(i.tolist())
            else:
                flat_idxs.append(int(i))
        top = ", ".join([str(term_names[i]) for i in flat_idxs])
        print(f"\nCluster {c}: {top}")
else:
    print("mbk.cluster_centers_ is not a numpy array, type:", type(mbk.cluster_centers_))

# ------------------------------------------------------------------
# 6) COMPLAINT EXTRACTION  (simple keyword demo)
# ------------------------------------------------------------------
compl_cache = cache_path("complaints.parquet")

if os.path.exists(compl_cache):
    complaints = pd.read_parquet(compl_cache)
    print("✅  complaints loaded")
else:
    NEG = ['高い','遅い','狭い','冷たい','ひどい','最悪',
           '問題','残念','不満','ミス','悪い']
    pat = '|'.join(NEG)
    complaints = df[df[TEXT_COL].str.contains(pat, na=False)]
    complaints.to_parquet(compl_cache)
    print("🆕  complaints cached :", len(complaints))

print("\n🎉  Pipeline done – cached artefacts are in /cache")