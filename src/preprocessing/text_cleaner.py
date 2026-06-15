"""Reusable text preprocessing pipeline."""

from __future__ import annotations

import html
import re
import string
from functools import lru_cache

import pandas as pd
from bs4 import BeautifulSoup

try:
    import nltk
    from nltk.corpus import stopwords
except ImportError:  # pragma: no cover - exercised only when optional deps are absent
    nltk = None
    stopwords = None

try:
    import spacy
except ImportError:  # pragma: no cover
    spacy = None

URL_PATTERN = re.compile(r"https?://\S+|www\.\S+")
EMOJI_PATTERN = re.compile(
    "["
    "\U0001f600-\U0001f64f"
    "\U0001f300-\U0001f5ff"
    "\U0001f680-\U0001f6ff"
    "\U0001f1e0-\U0001f1ff"
    "]+",
    flags=re.UNICODE,
)


@lru_cache(maxsize=1)
def _stop_words() -> set[str]:
    fallback = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "but",
        "for",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "the",
        "to",
        "with",
    }
    if nltk is None or stopwords is None:
        return fallback
    try:
        return set(stopwords.words("english"))
    except LookupError:
        nltk.download("stopwords", quiet=True)
        return set(stopwords.words("english"))


@lru_cache(maxsize=1)
def _nlp():
    if spacy is None:
        return None
    try:
        return spacy.load("en_core_web_sm", disable=["parser", "ner"])
    except OSError:
        return None


def clean_text(text: object, remove_stopwords: bool = True, lemmatize: bool = True) -> str:
    """Clean a text value for NLP modeling."""
    if pd.isna(text):
        return ""

    value = html.unescape(str(text).lower())
    value = BeautifulSoup(value, "html.parser").get_text(" ")
    value = URL_PATTERN.sub(" ", value)
    value = EMOJI_PATTERN.sub(" ", value)
    value = value.translate(str.maketrans("", "", string.punctuation))
    value = re.sub(r"\d+", " ", value)
    value = re.sub(r"\s+", " ", value).strip()

    tokens = value.split()
    if remove_stopwords:
        stops = _stop_words()
        tokens = [token for token in tokens if token not in stops]

    if lemmatize and tokens:
        nlp = _nlp()
        if nlp is not None:
            return " ".join(token.lemma_ for token in nlp(" ".join(tokens)))

    return " ".join(tokens)


def preprocess_posts(posts: pd.DataFrame) -> pd.DataFrame:
    """Clean Reddit posts and remove unusable rows."""
    frame = posts.copy()
    frame["text"] = (
        frame.get("title", pd.Series(dtype=str)).fillna("")
        + " "
        + frame.get("selftext", pd.Series(dtype=str)).fillna("")
    )
    frame["clean_text"] = frame["text"].apply(clean_text)
    frame["created_utc"] = pd.to_datetime(frame["created_utc"], errors="coerce", utc=True)
    frame = frame.dropna(subset=["created_utc"]).drop_duplicates(subset=["post_id"])
    return frame[frame["clean_text"].str.len() > 0].reset_index(drop=True)


def preprocess_comments(comments: pd.DataFrame) -> pd.DataFrame:
    """Clean Reddit comments and remove unusable rows."""
    frame = comments.copy()
    frame["text"] = frame.get("body", pd.Series(dtype=str)).fillna("")
    frame["clean_text"] = frame["text"].apply(clean_text)
    frame["created_utc"] = pd.to_datetime(frame["created_utc"], errors="coerce", utc=True)
    frame = frame.dropna(subset=["created_utc"]).drop_duplicates(subset=["comment_id"])
    return frame[frame["clean_text"].str.len() > 0].reset_index(drop=True)
