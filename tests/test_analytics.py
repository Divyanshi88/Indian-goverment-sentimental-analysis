import pandas as pd

from src.analytics.aggregations import sentiment_summary, sentiment_timeline


def test_sentiment_summary_percentages():
    frame = pd.DataFrame({"sentiment": ["positive", "positive", "negative"]})

    summary = sentiment_summary(frame)

    assert int(summary["count"].sum()) == 3
    assert round(float(summary["percentage"].sum()), 6) == 100.0


def test_sentiment_timeline_groups_by_day():
    frame = pd.DataFrame(
        {
            "created_utc": ["2026-05-20T10:00:00+00:00", "2026-05-20T11:00:00+00:00"],
            "sentiment": ["positive", "negative"],
        }
    )

    timeline = sentiment_timeline(frame, "D")

    assert set(timeline["sentiment"]) == {"positive", "negative"}
