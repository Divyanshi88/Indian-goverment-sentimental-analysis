"""Helper script to pre-label articles using keyword heuristics."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.utils.logging import get_logger

logger = get_logger(__name__)


# Sentiment keywords
POSITIVE_KEYWORDS = {
    "growth", "improve", "success", "strong", "gain", "progress",
    "recover", "boost", "surge", "jump", "positive", "advantage",
    "benefit", "reform", "innovation", "develop", "expand", "thrive",
    "prosperity", "opportunity", "efficient", "effective", "leading",
}

NEGATIVE_KEYWORDS = {
    "decline", "fall", "fail", "crisis", "problem", "loss", "weak",
    "drop", "collapse", "crash", "negative", "disadvantage", "harm",
    "risk", "threat", "challenge", "struggle", "concern", "issue",
    "dispute", "conflict", "corruption", "scandal", "debt", "recession",
}

# Stop words to ignore
STOP_WORDS = {
    "the", "a", "an", "and", "or", "but", "in", "on", "at", "to",
    "is", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "do", "does", "did", "will", "would", "could", "should",
    "may", "might", "must", "can", "for", "of", "with", "by", "from",
}


def extract_keywords(text: str) -> set[str]:
    """Extract keywords from text."""
    if not isinstance(text, str):
        return set()
    
    words = text.lower().split()
    return {w.strip('.,!?;:') for w in words if w.lower() not in STOP_WORDS and len(w) > 3}


def predict_sentiment(title: str, description: str) -> tuple[str, float]:
    """
    Predict sentiment based on keywords.

    Returns:
        (sentiment, confidence) where confidence is 0-1
    """
    text = f"{title} {description}".lower()
    keywords = extract_keywords(text)

    positive_matches = len(keywords & POSITIVE_KEYWORDS)
    negative_matches = len(keywords & NEGATIVE_KEYWORDS)

    total_matches = positive_matches + negative_matches

    if total_matches == 0:
        return "neutral", 0.0

    pos_ratio = positive_matches / total_matches
    confidence = total_matches / (len(keywords) / 2) if keywords else 0

    if pos_ratio > 0.65:
        return "positive", min(1.0, confidence)
    elif pos_ratio < 0.35:
        return "negative", min(1.0, confidence)
    else:
        return "neutral", min(1.0, confidence)


def auto_label_articles(
    input_path: Path | None = None,
    output_path: Path | None = None,
    confidence_threshold: float = 0.6,
) -> pd.DataFrame:
    """
    Auto-label articles using keyword-based heuristics.

    Args:
        input_path: Path to CSV with articles
        output_path: Path to save labeled CSV
        confidence_threshold: Minimum confidence to auto-label (0-1)

    Returns:
        DataFrame with predictions
    """
    if input_path is None:
        input_path = PROJECT_ROOT / "data" / "raw" / "newsapi_training.csv"
    if output_path is None:
        output_path = input_path  # Overwrite original

    logger.info("=" * 70)
    logger.info("AUTO-LABELING ARTICLES WITH KEYWORD HEURISTICS")
    logger.info("=" * 70)

    # Load data
    df = pd.read_csv(input_path)
    logger.info(f"Loaded {len(df)} articles")

    # Predict sentiment
    logger.info(f"\nPredicting sentiment (confidence threshold: {confidence_threshold})...")

    predictions = []
    for _, row in df.iterrows():
        sentiment, confidence = predict_sentiment(
            row.get("title", ""),
            row.get("description", ""),
        )
        predictions.append({
            "sentiment": sentiment,
            "confidence": confidence,
        })

    predictions_df = pd.DataFrame(predictions)

    # Update dataframe
    df["sentiment_predicted"] = predictions_df["sentiment"]
    df["confidence"] = predictions_df["confidence"]

    # Only auto-label high confidence predictions
    high_confidence = df[df["confidence"] >= confidence_threshold]
    df.loc[high_confidence.index, "sentiment"] = high_confidence["sentiment_predicted"]
    df.loc[high_confidence.index, "labeled"] = False  # Still mark as needing review

    # Save
    df.to_csv(output_path, index=False)

    logger.info(f"\n✓ Saved to {output_path}")

    # Summary
    summary = df.groupby("sentiment").size()
    logger.info(f"\nPredicted sentiment distribution:")
    for sentiment, count in summary.items():
        logger.info(f"  {sentiment}: {count}")

    high_conf_count = (df["confidence"] >= confidence_threshold).sum()
    logger.info(f"\nHigh confidence predictions (>={confidence_threshold}): {high_conf_count}")
    logger.info(f"Still need manual review: {len(df) - high_conf_count}")

    return df


def create_sample_labeled_data(output_path: Path | None = None) -> None:
    """
    Create a sample labeled dataset for testing/demonstration.
    """
    if output_path is None:
        output_path = PROJECT_ROOT / "data" / "raw" / "sample_labeled.csv"

    sample_articles = [
        {
            "title": "India's Economy Shows Strong Growth in Q2",
            "description": "New data reveals impressive economic expansion with GDP growth at 6.5%",
            "sentiment": "positive",
            "labeled": True,
        },
        {
            "title": "Government Announces Major Policy Reforms",
            "description": "New legislation aims to improve business efficiency and competitiveness",
            "sentiment": "positive",
            "labeled": True,
        },
        {
            "title": "Budget Surplus Helps Reduce National Debt",
            "description": "Financial reports show positive progress in fiscal management",
            "sentiment": "positive",
            "labeled": True,
        },
        {
            "title": "Parliament Debates New Cabinet Appointments",
            "description": "Government introduces new leadership team to parliament for approval",
            "sentiment": "neutral",
            "labeled": True,
        },
        {
            "title": "Election Commission Announces Voting Dates",
            "description": "Official announcement of schedule for upcoming general elections",
            "sentiment": "neutral",
            "labeled": True,
        },
        {
            "title": "Ministry Releases Annual Report",
            "description": "Department provides detailed report on activities and progress",
            "sentiment": "neutral",
            "labeled": True,
        },
        {
            "title": "Economic Crisis Deepens as Inflation Soars",
            "description": "Rising prices create significant hardship for citizens and businesses",
            "sentiment": "negative",
            "labeled": True,
        },
        {
            "title": "Government Policy Faces Strong Opposition",
            "description": "Critics argue new legislation will harm the economy and citizens",
            "sentiment": "negative",
            "labeled": True,
        },
        {
            "title": "Prime Minister's Approval Rating Plummets",
            "description": "Latest polls show declining public support for current administration",
            "sentiment": "negative",
            "labeled": True,
        },
    ]

    df = pd.DataFrame(sample_articles)
    
    # Add required columns
    df["article_id"] = [f"sample_{i}" for i in range(len(df))]
    df["source_name"] = "Sample Data"
    df["clean_text"] = (df["title"] + " " + df["description"]).str.lower()
    df["notes"] = ""
    df["published_at"] = "2026-06-16T00:00:00Z"
    df["url"] = "https://example.com"

    # Reorder columns
    columns = [
        "article_id", "source_name", "title", "description", "clean_text",
        "sentiment", "labeled", "notes", "published_at", "url"
    ]
    df = df[columns]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)

    logger.info(f"✓ Sample labeled data created: {output_path}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Auto-label articles using keywords")
    parser.add_argument(
        "--mode",
        choices=["predict", "sample"],
        default="predict",
        help="Mode: 'predict' to auto-label or 'sample' to create sample data",
    )
    parser.add_argument(
        "--input",
        type=Path,
        help="Input CSV path",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output CSV path",
    )
    parser.add_argument(
        "--confidence",
        type=float,
        default=0.6,
        help="Confidence threshold for auto-labeling (0-1)",
    )

    args = parser.parse_args()

    if args.mode == "sample":
        create_sample_labeled_data(args.output)
    else:
        auto_label_articles(
            input_path=args.input,
            output_path=args.output,
            confidence_threshold=args.confidence,
        )
