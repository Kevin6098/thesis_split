# src/stop_words.py
# ------------------------------------------------------------------
# Master list of Japanese stop-words, interjections, HTML fragments,
# emoji, filler phrases, etc.  Feel free to extend or prune.

import re

JP_STOPWORDS = {
    # 感動詞・間投詞
    "ああ", "あら", "ありゃ", "あれ", "おお", "おっと", "おや", "うん", "ええ", "えっ",
    "わあ", "わー", "うわ", "はっ", "やれやれ", "へえ", "ほう", "よし", "なるほど",
    "さあ", "さて", "では", "おっ", "ほら",
    # 代名詞（指示・人称）
    "これ", "それ", "あれ", "どれ",
    "ここ", "そこ", "あそこ", "どこ",
    "こちら", "そちら", "あちら", "どちら",
    "こっち", "そっち", "あっち", "どっち",
    "わたし", "私", "わたくし", "ぼく", "僕", "おれ", "俺",
    "あなた", "きみ", "君", "おまえ",
    "彼", "彼女", "かれら", "かのじょら",
    "われわれ", "私たち", "みんな", "誰", "だれ",
    # 形容詞（非自立）・接尾的評価語
    "らしい", "っぽい", "げ", "がち", "め", "っけ", "ず", "なし", "まま",
    # 副詞可能（名詞由来副詞・強調語）
    "とても", "かなり", "すごく", "けっこう", "もっと", "ほとんど",
    "たぶん", "きっと", "まったく", "ぜひ", "まず", "もちろん",
    "いきなり", "やはり", "やっぱり", "つまり",
    # HTMLタグ・マークアップ断片
    "<br>", "</br>", "<br/>", "<p>", "</p>", "<div>", "</div>",
    "<span>", "</span>", "<ul>", "</ul>", "<li>", "</li>",
    "<strong>", "</strong>", "<em>", "</em>",
    "&nbsp;", "&lt;", "&gt;", "&amp;",
    # URLs and fragments
    "http", "https", "www",
    # 未知語・記号・絵文字っぽい文字列
    "w", "ww", "www", "ｗ", "笑", "(笑)", "泣", "汗",
    "＼(^o^)／", "(^_^)", "(^o^)", "※", "♪", "☆", "★",
    "♡", "❤", "😂", "🤣", "👍", "👎", "😊", "😢",
    # その他の頻出ノイズ
    "とか", "なんか", "など", "なんて", "だとか", "とかで",
    "などの", "などが", "こと", "さん"
}

def get_cleaned_stopwords():
    # Only keep words that match the token pattern (alphanumeric/underscore, no HTML or special chars)
    token_pattern = re.compile(r"^\w+$", re.UNICODE)
    cleaned = set()
    for word in JP_STOPWORDS:
        if token_pattern.match(word):
            cleaned.add(word)
    return cleaned

# Back-compat alias — modules that still import STOP_WORDS will work
STOP_WORDS = get_cleaned_stopwords()