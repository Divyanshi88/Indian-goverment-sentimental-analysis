"""Dashboard-ready analytics transformations."""

from __future__ import annotations

import pandas as pd


def combine_content(posts: pd.DataFrame, comments: pd.DataFrame) -> pd.DataFrame:
    """Combine posts and comments into one analytics table."""
    post_cols = [
        "post_id",
        "subreddit",
        "text",
        "clean_text",
        "score",
        "author",
        "created_utc",
        "sentiment",
        "sentiment_probability",
        "permalink",
    ]
    comment_cols = [
        "comment_id",
        "post_id",
        "subreddit",
        "text",
        "clean_text",
        "score",
        "author",
        "created_utc",
        "sentiment",
        "sentiment_probability",
        "permalink",
    ]
    post_frame = posts[[col for col in post_cols if col in posts.columns]].copy()
    post_frame["content_type"] = "post"
    comment_frame = comments[[col for col in comment_cols if col in comments.columns]].copy()
    comment_frame["content_type"] = "comment"
    return pd.concat([post_frame, comment_frame], ignore_index=True, sort=False)


def sentiment_summary(frame: pd.DataFrame) -> pd.DataFrame:
    """Calculate sentiment counts and percentages."""
    counts = frame["sentiment"].value_counts().rename_axis("sentiment").reset_index(name="count")
    counts["percentage"] = counts["count"] / counts["count"].sum() * 100
    return counts


def sentiment_timeline(frame: pd.DataFrame, frequency: str = "D") -> pd.DataFrame:
    """Aggregate sentiment counts by date frequency."""
    output = frame.copy()
    output["created_utc"] = pd.to_datetime(output["created_utc"], utc=True)
    timeline = (
        output.groupby(["sentiment", pd.Grouper(key="created_utc", freq=frequency)])
        .size()
        .rename("count")
        .reset_index()
    )
    timeline["period"] = timeline["created_utc"].dt.date
    return timeline
