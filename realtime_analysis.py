"""Script to analyze real-time news sentiment with trained models using NewsAPI."""

from __future__ import annotations

import os
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.models.realtime_news_analyzer import RealtimeNewsAnalyzer
from src.utils.logging import get_logger

logger = get_logger(__name__)


def analyze_recent_news_sentiment(
    queries: list[str] | None = None,
    days_back: int = 7,
    page_size: int = 100,
    model: str = "logistic_regression",
    api_key: str | None = None,
) -> None:
    """
    Analyze recent news articles for sentiment.

    Args:
        queries: Search queries (default: government-related topics)
        days_back: Number of days back to search
        page_size: Number of articles per query
        model: Model to use ('logistic_regression' or 'naive_bayes')
        api_key: NewsAPI key (if None, reads from NEWSAPI_KEY env var)
    """
    if queries is None:
        queries = [
            "government",
            "election",
            "policy",
            "budget",
            "parliament",
            "prime minister",
            "indian government",
            "ministry",
            "cabinet",
            "legislation",
        ]

    logger.info("=" * 70)
    logger.info("REAL-TIME NEWS SENTIMENT ANALYSIS")
    logger.info("=" * 70)

    # Initialize analyzer
    analyzer = RealtimeNewsAnalyzer(api_key=api_key, model_name=model)

    # Connect to NewsAPI
    if not analyzer.connect_newsapi():
        logger.error("Failed to connect to NewsAPI. Check your API key.")
        logger.info("Set environment variable: NEWSAPI_KEY")
        return

    # Search and analyze articles
    logger.info(f"\n{'=' * 70}")
    logger.info(f"SEARCHING FOR ARTICLES")
    logger.info(f"Queries: {', '.join(queries)}")
    logger.info(f"Days back: {days_back}")
    logger.info("=" * 70)
    
    articles_df = analyzer.search_and_analyze(
        queries=queries,
        days_back=days_back,
        page_size=page_size,
    )
    
    if not articles_df.empty:
        summary = analyzer.get_sentiment_summary(articles_df)
        logger.info(f"\nArticle Sentiment Summary:")
        logger.info(f"  Total Articles: {summary['total']}")
        logger.info(f"  Positive: {summary['positive']}")
        logger.info(f"  Negative: {summary['negative']}")
        logger.info(f"  Neutral: {summary['neutral']}")
        logger.info(f"  Avg Probability: {summary['avg_probability']:.3f}")
        
        # Save articles
        articles_output = Path("realtime_articles_analysis.csv")
        articles_df.to_csv(articles_output, index=False)
        logger.info(f"\nArticles saved to {articles_output}")
        
        # Display sample
        logger.info(f"\nSample Articles:")
        for idx, row in articles_df.head(5).iterrows():
            logger.info(f"  [{idx+1}] {row['sentiment'].upper()}: {row['title'][:60]}...")
            logger.info(f"       Source: {row['source_name']} | Prob: {row['sentiment_probability']:.3f}")
    else:
        logger.warning("No articles found")

    # Analyze top headlines
    logger.info(f"\n{'=' * 70}")
    logger.info(f"ANALYZING TOP HEADLINES (India)")
    logger.info("=" * 70)
    
    headlines_df = analyzer.analyze_top_headlines(country="in", page_size=20)
    
    if not headlines_df.empty:
        headline_summary = analyzer.get_sentiment_summary(headlines_df)
        logger.info(f"\nHeadline Sentiment Summary:")
        logger.info(f"  Total Headlines: {headline_summary['total']}")
        logger.info(f"  Positive: {headline_summary['positive']}")
        logger.info(f"  Negative: {headline_summary['negative']}")
        logger.info(f"  Neutral: {headline_summary['neutral']}")
        logger.info(f"  Avg Probability: {headline_summary['avg_probability']:.3f}")
        
        # Save headlines
        headlines_output = Path("realtime_headlines_analysis.csv")
        headlines_df.to_csv(headlines_output, index=False)
        logger.info(f"\nHeadlines saved to {headlines_output}")
        
        # Display sample
        logger.info(f"\nSample Headlines:")
        for idx, row in headlines_df.head(5).iterrows():
            logger.info(f"  [{idx+1}] {row['sentiment'].upper()}: {row['title'][:60]}...")
    else:
        logger.warning("No headlines found")

    # Combined analysis
    logger.info(f"\n{'=' * 70}")
    logger.info("COMBINED ANALYSIS")
    logger.info("=" * 70)
    
    if not articles_df.empty and not headlines_df.empty:
        combined_df = pd.concat([articles_df, headlines_df], ignore_index=True)
        combined_summary = analyzer.get_sentiment_summary(combined_df)
        logger.info(f"\nCombined Sentiment Distribution:")
        logger.info(f"  Total Items: {combined_summary['total']}")
        logger.info(f"  Positive: {combined_summary['positive']}")
        logger.info(f"  Negative: {combined_summary['negative']}")
        logger.info(f"  Neutral: {combined_summary['neutral']}")
        logger.info(f"  Avg Probability: {combined_summary['avg_probability']:.3f}")
        
        # Save combined
        combined_output = Path("realtime_combined_analysis.csv")
        combined_df.to_csv(combined_output, index=False)
        logger.info(f"\nCombined data saved to {combined_output}")



def stream_news_sentiment(
    queries: list[str] | None = None,
    days_back: int = 1,
    page_size: int = 50,
    model: str = "logistic_regression",
    api_key: str | None = None,
) -> None:
    """
    Stream news sentiment updates continuously.

    Args:
        queries: Search queries
        days_back: Number of days back to search
        page_size: Number of articles per query
        model: Model to use ('logistic_regression' or 'naive_bayes')
        api_key: NewsAPI key
    """
    if queries is None:
        queries = [
            "government",
            "election",
            "policy",
            "parliament",
            "prime minister",
        ]

    logger.info("=" * 70)
    logger.info("STREAMING NEWS SENTIMENT")
    logger.info("=" * 70)

    # Initialize analyzer
    analyzer = RealtimeNewsAnalyzer(api_key=api_key, model_name=model)

    # Connect to NewsAPI
    if not analyzer.connect_newsapi():
        logger.error("Failed to connect to NewsAPI. Check your API key.")
        return

    logger.info(f"\nStreaming news with queries: {', '.join(queries)}")
    logger.info("Press Ctrl+C to stop\n")

    # Stream articles
    try:
        stream_df = analyzer.search_and_analyze(
            queries=queries,
            days_back=days_back,
            page_size=page_size,
        )
        
        if not stream_df.empty:
            summary = analyzer.get_sentiment_summary(stream_df)
            logger.info(f"\n{'=' * 70}")
            logger.info("STREAMING SUMMARY")
            logger.info("=" * 70)
            logger.info(f"Total Articles: {summary['total']}")
            logger.info(f"Positive: {summary['positive']}")
            logger.info(f"Negative: {summary['negative']}")
            logger.info(f"Neutral: {summary['neutral']}")
            logger.info(f"Avg Probability: {summary['avg_probability']:.3f}")
            
            # Save streaming results
            output = Path("realtime_stream_analysis.csv")
            stream_df.to_csv(output, index=False)
            logger.info(f"\nResults saved to {output}")
    except KeyboardInterrupt:
        logger.info("\nStreaming stopped by user")



if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Real-time news sentiment analysis using NewsAPI")
    parser.add_argument(
        "--mode",
        choices=["recent", "stream"],
        default="recent",
        help="Analysis mode: 'recent' for recent articles or 'stream' for continuous updates",
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
        help="Number of articles per query (default: 100, max 100)",
    )
    parser.add_argument(
        "--queries",
        nargs="+",
        help="Search queries (default: government-related topics)",
    )
    parser.add_argument(
        "--model",
        choices=["logistic_regression", "naive_bayes"],
        default="logistic_regression",
        help="Model to use (default: logistic_regression)",
    )

    args = parser.parse_args()

    # Validate API key
    api_key = args.api_key or os.getenv("NEWSAPI_KEY")
    if not api_key:
        logger.error("NewsAPI key not found!")
        logger.error("Please set NEWSAPI_KEY environment variable or use --api-key argument")
        sys.exit(1)

    if args.mode == "recent":
        analyze_recent_news_sentiment(
            queries=args.queries,
            days_back=args.days_back,
            page_size=args.page_size,
            model=args.model,
            api_key=api_key,
        )
    else:
        stream_news_sentiment(
            queries=args.queries,
            days_back=1,  # For streaming, use shorter lookback
            page_size=args.page_size,
            model=args.model,
            api_key=api_key,
        )
