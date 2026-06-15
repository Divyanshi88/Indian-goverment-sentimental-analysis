"""Command line entry point for the local pipeline."""

from __future__ import annotations

from pathlib import Path

from src.analytics.aggregations import combine_content
from src.data_collection.sample_data import write_sample_data
from src.models.sentiment import add_sentiment_labels
from src.preprocessing.text_cleaner import preprocess_comments, preprocess_posts
from src.utils.config import ROOT_DIR
from src.utils.logging import get_logger

logger = get_logger(__name__)


def run_sample_pipeline() -> Path:
    """Run the end-to-end pipeline on bundled sample data."""
    posts_path, comments_path = write_sample_data(ROOT_DIR / "data")
    logger.info("Wrote sample raw data to %s and %s", posts_path, comments_path)

    import pandas as pd

    posts = add_sentiment_labels(preprocess_posts(pd.read_csv(posts_path)))
    comments = add_sentiment_labels(preprocess_comments(pd.read_csv(comments_path)))
    analytics = combine_content(posts, comments)

    processed_dir = ROOT_DIR / "data" / "processed"
    processed_dir.mkdir(parents=True, exist_ok=True)
    output_path = processed_dir / "sentiment_content.csv"
    analytics.to_csv(output_path, index=False)
    posts.to_csv(processed_dir / "processed_posts.csv", index=False)
    comments.to_csv(processed_dir / "processed_comments.csv", index=False)
    logger.info("Wrote processed analytics table to %s", output_path)
    return output_path


if __name__ == "__main__":
    run_sample_pipeline()
