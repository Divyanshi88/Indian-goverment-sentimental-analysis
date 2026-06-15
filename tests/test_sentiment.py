import pandas as pd

from src.models.sentiment import add_sentiment_labels, lexicon_sentiment


def test_lexicon_sentiment_detects_positive():
    label, probability = lexicon_sentiment("good improvement jobs relief")

    assert label == "positive"
    assert probability > 0.5


def test_add_sentiment_labels_creates_columns():
    frame = pd.DataFrame({"clean_text": ["weak delay failure", "good relief"]})

    output = add_sentiment_labels(frame)

    assert {"sentiment", "sentiment_probability"}.issubset(output.columns)
    assert list(output["sentiment"]) == ["negative", "positive"]
