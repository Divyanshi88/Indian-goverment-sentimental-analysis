"""Keyword extraction and topic modeling."""

from __future__ import annotations

import pandas as pd
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


def extract_tfidf_keywords(
    frame: pd.DataFrame,
    text_column: str = "clean_text",
    top_n: int = 20,
) -> pd.DataFrame:
    """Extract corpus-level keywords with TF-IDF."""
    vectorizer = TfidfVectorizer(max_features=1000, ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(frame[text_column].fillna(""))
    scores = matrix.mean(axis=0).A1
    keywords = pd.DataFrame({"keyword": vectorizer.get_feature_names_out(), "score": scores})
    return keywords.sort_values("score", ascending=False).head(top_n).reset_index(drop=True)


def lda_topics(
    frame: pd.DataFrame,
    text_column: str = "clean_text",
    n_topics: int = 4,
    top_n_words: int = 8,
) -> pd.DataFrame:
    """Create topic clusters using LDA."""
    texts = frame[text_column].fillna("")
    vectorizer = CountVectorizer(max_df=0.95, min_df=1, stop_words="english")
    matrix = vectorizer.fit_transform(texts)
    if matrix.shape[1] == 0:
        return pd.DataFrame(columns=["topic", "keywords"])

    topic_count = min(n_topics, max(1, matrix.shape[0]))
    lda = LatentDirichletAllocation(n_components=topic_count, random_state=42)
    lda.fit(matrix)
    words = vectorizer.get_feature_names_out()

    topics = []
    for topic_idx, topic in enumerate(lda.components_):
        top_words = [words[index] for index in topic.argsort()[-top_n_words:][::-1]]
        topics.append({"topic": f"Topic {topic_idx + 1}", "keywords": ", ".join(top_words)})
    return pd.DataFrame(topics)
