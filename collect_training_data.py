"""Collect real-time news data from NewsAPI for model training."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data_collection.newsapi_client import create_newsapi_client
from src.preprocessing.text_cleaner import clean_text
from src.utils.logging import get_logger

logger = get_logger(__name__)


def collect_newsapi_training_data(
    api_key: str | None = None,
    days_back: int = 7,
    page_size: int = 100,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """
    Collect news articles from NewsAPI for training data.

    Args:
        api_key: NewsAPI key (if None, reads from NEWSAPI_KEY env var)
        days_back: Number of days back to search
        page_size: Articles per query
        output_path: Where to save the CSV (default: data/raw/newsapi_training.csv)

    Returns:
        DataFrame with collected articles
    """
    if output_path is None:
        output_path = PROJECT_ROOT / "data" / "raw" / "newsapi_training.csv"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)

    logger.info("=" * 70)
    logger.info("COLLECTING TRAINING DATA FROM NEWSAPI")
    logger.info("=" * 70)

    # Create client
    try:
        client = create_newsapi_client(api_key=api_key)
        logger.info("✓ Connected to NewsAPI")
    except RuntimeError as e:
        logger.error(f"Failed to connect to NewsAPI: {e}")
        return pd.DataFrame()

    # Search queries related to government
    queries = [
        "government",
        "election",
        "policy",
        "parliament",
        "prime minister",
        "cabinet",
        "ministry",
        "legislation",
        "budget",
        "inflation",
        "economy",
        "development",
        "regulation",
        "reform",
    ]

    logger.info(f"\nSearching for {len(queries)} query topics...")
    articles_df = client.search_articles(
        queries=queries,
        language="en",
        sort_by="publishedAt",
        page_size=page_size,
        days_back=days_back,
    )

    if articles_df.empty:
        logger.error("No articles found")
        return pd.DataFrame()

    logger.info(f"✓ Collected {len(articles_df)} articles")

    # Add clean_text column for preprocessing consistency
    logger.info("Preprocessing text...")
    articles_df["clean_text"] = articles_df.apply(
        lambda row: clean_text(f"{row['title']} {row['description']}"),
        axis=1,
    )

    # Initialize sentiment as neutral (baseline)
    # Users can manually label these
    articles_df["sentiment"] = "neutral"
    articles_df["labeled"] = False  # Mark as not manually labeled
    articles_df["notes"] = ""

    # Keep relevant columns for training
    training_df = articles_df[[
        "article_id",
        "source_name",
        "title",
        "description",
        "clean_text",
        "sentiment",
        "labeled",
        "notes",
        "published_at",
        "url",
    ]]

    # Save to CSV
    training_df.to_csv(output_path, index=False)
    logger.info(f"✓ Saved {len(training_df)} articles to {output_path}")

    logger.info("\n" + "=" * 70)
    logger.info("NEXT STEPS")
    logger.info("=" * 70)
    logger.info(f"1. Open {output_path} in a spreadsheet application")
    logger.info("2. Review articles and update 'sentiment' column:")
    logger.info("   - 'positive' for positive government/policy sentiment")
    logger.info("   - 'negative' for negative government/policy sentiment")
    logger.info("   - 'neutral' for neutral/informational content")
    logger.info("3. Update 'labeled' column to True when done")
    logger.info("4. Run: python retrain_models.py")

    return training_df


def combine_training_data(
    newsapi_path: Path | None = None,
    original_path: Path | None = None,
    sample_path: Path | None = None,
    output_path: Path | None = None,
) -> pd.DataFrame:
    """
    Combine original training data with newly collected NewsAPI data.

    Args:
        newsapi_path: Path to NewsAPI training CSV
        original_path: Path to original training CSV
        sample_path: Path to sample labeled CSV
        output_path: Where to save combined data

    Returns:
        Combined DataFrame
    """
    if newsapi_path is None:
        newsapi_path = PROJECT_ROOT / "data" / "raw" / "newsapi_training.csv"
    if original_path is None:
        original_path = PROJECT_ROOT / "data" / "processed" / "sentiment_content.csv"
    if sample_path is None:
        sample_path = PROJECT_ROOT / "data" / "raw" / "sample_labeled.csv"
    if output_path is None:
        output_path = PROJECT_ROOT / "data" / "processed" / "combined_training.csv"

    logger.info("=" * 70)
    logger.info("COMBINING TRAINING DATA")
    logger.info("=" * 70)

    dfs = []

    # Load original data
    if original_path.exists():
        try:
            original_df = pd.read_csv(original_path)
            # Standardize to clean_text and sentiment columns
            if "clean_text" not in original_df.columns:
                from src.preprocessing.text_cleaner import clean_text
                original_df["clean_text"] = original_df.apply(
                    lambda row: clean_text(f"{row.get('text', '')} {row.get('title', '')}"),
                    axis=1,
                )
            logger.info(f"✓ Loaded {len(original_df)} original samples")
            dfs.append(original_df[["clean_text", "sentiment"]])
        except Exception as e:
            logger.error(f"Error loading original data: {e}")

    # Load sample data first (takes precedence if labeled)
    if sample_path.exists():
        try:
            sample_df = pd.read_csv(sample_path)
            # Filter to only labeled samples
            labeled_col = sample_df.get("labeled", [False])
            if "labeled" in sample_df.columns:
                if isinstance(labeled_col.iloc[0] if len(labeled_col) > 0 else False, str):
                    labeled_mask = sample_df["labeled"].astype(str).str.lower() == "true"
                else:
                    labeled_mask = sample_df["labeled"] == True
                labeled_df = sample_df[labeled_mask]
            else:
                labeled_df = sample_df
            
            if len(labeled_df) > 0:
                logger.info(f"✓ Loaded {len(labeled_df)} labeled sample articles")
                # Ensure clean_text column exists
                if "clean_text" not in labeled_df.columns:
                    from src.preprocessing.text_cleaner import clean_text
                    labeled_df = labeled_df.copy()
                    labeled_df["clean_text"] = labeled_df.apply(
                        lambda row: clean_text(f"{row.get('title', '')} {row.get('description', '')}"),
                        axis=1,
                    )
                dfs.append(labeled_df[["clean_text", "sentiment"]])
        except Exception as e:
            logger.error(f"Error loading sample data: {e}")

    # Load NewsAPI data - only use labeled articles
    if newsapi_path.exists():
        try:
            newsapi_df = pd.read_csv(newsapi_path)
            # Filter to only labeled articles (handle both boolean and string "True")
            labeled_col = newsapi_df.get("labeled", [False])
            # Convert to boolean if string
            if isinstance(labeled_col.iloc[0] if len(labeled_col) > 0 else False, str):
                labeled_mask = newsapi_df["labeled"].astype(str).str.lower() == "true"
            else:
                labeled_mask = newsapi_df["labeled"] == True
            labeled_df = newsapi_df[labeled_mask]
            if len(labeled_df) > 0:
                logger.info(f"✓ Loaded {len(labeled_df)} labeled NewsAPI samples")
                # Ensure clean_text column exists
                if "clean_text" not in labeled_df.columns:
                    from src.preprocessing.text_cleaner import clean_text
                    labeled_df = labeled_df.copy()
                    labeled_df["clean_text"] = labeled_df.apply(
                        lambda row: clean_text(f"{row.get('title', '')} {row.get('description', '')}"),
                        axis=1,
                    )
                dfs.append(labeled_df[["clean_text", "sentiment"]])
        except Exception as e:
            logger.error(f"Error loading NewsAPI data: {e}")

    if not dfs:
        logger.error("No data sources available")
        return pd.DataFrame()

    # Combine
    combined_df = pd.concat(dfs, ignore_index=True)

    # Save
    output_path.parent.mkdir(parents=True, exist_ok=True)
    combined_df.to_csv(output_path, index=False)
    logger.info(f"\n✓ Combined dataset saved to {output_path}")
    logger.info(f"  Total samples: {len(combined_df)}")
    logger.info(f"  Sentiment distribution:\n{combined_df['sentiment'].value_counts()}")

    return combined_df


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Collect training data from NewsAPI"
    )
    parser.add_argument(
        "--mode",
        choices=["collect", "combine"],
        default="collect",
        help="Mode: 'collect' to fetch new articles or 'combine' to merge datasets",
    )
    parser.add_argument(
        "--api-key",
        help="NewsAPI key (if not set, reads from NEWSAPI_KEY env var)",
    )
    parser.add_argument(
        "--days-back",
        type=int,
        default=7,
        help="Number of days back to search (default: 7)",
    )
    parser.add_argument(
        "--page-size",
        type=int,
        default=100,
        help="Articles per query (default: 100)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output CSV path",
    )

    args = parser.parse_args()

    if args.mode == "collect":
        api_key = args.api_key or os.getenv("NEWSAPI_KEY")
        if not api_key:
            logger.error("NewsAPI key required. Set NEWSAPI_KEY or use --api-key")
            sys.exit(1)

        collect_newsapi_training_data(
            api_key=api_key,
            days_back=args.days_back,
            page_size=args.page_size,
            output_path=args.output,
        )
    else:
        combine_training_data(output_path=args.output)
