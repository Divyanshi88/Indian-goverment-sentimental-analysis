"""News ingestion using NewsAPI.org."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from datetime import datetime
from typing import Iterable

import pandas as pd
import requests

from src.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class NewsArticle:
    """Represents a news article from NewsAPI."""
    article_id: str
    source_name: str
    title: str
    description: str
    content: str
    author: str
    published_at: str
    url: str
    image_url: str
    sentiment_keywords: list[str]


def create_newsapi_client(api_key: str | None = None) -> NewsAPIClient:
    """Create a NewsAPI client from API key or environment variable."""
    if api_key is None:
        api_key = os.getenv("NEWSAPI_KEY")
    
    if not api_key:
        raise RuntimeError(
            "NewsAPI key not provided. Set NEWSAPI_KEY environment variable "
            "or pass api_key parameter."
        )
    
    return NewsAPIClient(api_key=api_key)


class NewsAPIClient:
    """Client for fetching news articles from NewsAPI.org."""

    BASE_URL = "https://newsapi.org/v2"
    ENDPOINTS = {
        "everything": f"{BASE_URL}/everything",
        "top_headlines": f"{BASE_URL}/top-headlines",
    }

    def __init__(self, api_key: str):
        """Initialize the NewsAPI client.
        
        Args:
            api_key: NewsAPI.org API key
        """
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Indian-Government-Sentiment-Analysis/1.0"
        })

    def search_articles(
        self,
        queries: Iterable[str],
        language: str = "en",
        sort_by: str = "publishedAt",
        page_size: int = 100,
        days_back: int = 7,
    ) -> pd.DataFrame:
        """
        Search for news articles related to specified queries.

        Args:
            queries: List of search queries (e.g., ["government", "election"])
            language: Language code (default: "en" for English)
            sort_by: Sort order ("publishedAt", "relevancy", "popularity")
            page_size: Number of articles per query (max 100)
            days_back: Number of days back to search

        Returns:
            DataFrame with articles
        """
        records: list[dict[str, object]] = []
        
        for query in queries:
            logger.info(f"Searching articles for: {query}")
            try:
                articles = self._search_everything(
                    q=query,
                    language=language,
                    sort_by=sort_by,
                    page_size=page_size,
                    days_back=days_back,
                )
                records.extend(articles)
            except Exception as e:
                logger.error(f"Error searching for '{query}': {e}")
                continue

        if not records:
            logger.warning("No articles found")
            return pd.DataFrame()

        return pd.DataFrame.from_records(records)

    def _search_everything(
        self,
        q: str,
        language: str = "en",
        sort_by: str = "publishedAt",
        page_size: int = 100,
        days_back: int = 7,
    ) -> list[dict[str, object]]:
        """
        Make request to /everything endpoint.

        Args:
            q: Search query
            language: Language code
            sort_by: Sort order
            page_size: Page size (max 100)
            days_back: Days back for from_date

        Returns:
            List of article dictionaries
        """
        from datetime import timedelta, timezone

        now = datetime.now(timezone.utc)
        from_date = now - timedelta(days=days_back)

        params = {
            "q": q,
            "language": language,
            "sortBy": sort_by,
            "pageSize": min(page_size, 100),
            "apiKey": self.api_key,
            "from": from_date.isoformat(),
            "to": now.isoformat(),
        }

        response = self.session.get(self.ENDPOINTS["everything"], params=params)
        response.raise_for_status()

        data = response.json()
        if data.get("status") != "ok":
            error_msg = data.get("message", "Unknown error")
            raise RuntimeError(f"NewsAPI error: {error_msg}")

        articles = []
        for i, article in enumerate(data.get("articles", [])):
            try:
                article_record = self._parse_article(article, query=q)
                articles.append(article_record)
            except Exception as e:
                logger.warning(f"Error parsing article: {e}")
                continue

        return articles

    def _parse_article(self, article: dict, query: str = "") -> dict[str, object]:
        """
        Parse a single article from API response.

        Args:
            article: Article dictionary from API
            query: Search query used to find this article

        Returns:
            Parsed article dictionary
        """
        # Create unique ID from source and URL
        source_name = article.get("source", {}).get("name", "Unknown")
        url = article.get("url", "")
        article_id = f"{source_name}_{hash(url) % 10000}"

        published_at = article.get("publishedAt", "")
        if published_at and "T" in published_at:
            # Ensure ISO format
            published_at = published_at.replace("Z", "+00:00")

        return {
            "article_id": article_id,
            "source_name": source_name,
            "title": article.get("title", ""),
            "description": article.get("description", ""),
            "content": article.get("content", ""),
            "author": article.get("author", "Unknown"),
            "published_at": published_at,
            "url": url,
            "image_url": article.get("urlToImage", ""),
            "sentiment_keywords": [query] if query else [],
        }

    def get_top_headlines(
        self,
        country: str = "in",
        category: str | None = None,
        page_size: int = 20,
    ) -> pd.DataFrame:
        """
        Get top headlines for a country.

        Args:
            country: Country code (e.g., "in" for India)
            category: Category filter (e.g., "general", "politics")
            page_size: Number of headlines (max 100)

        Returns:
            DataFrame with headlines
        """
        logger.info(f"Fetching top headlines for {country}")

        params = {
            "country": country,
            "pageSize": min(page_size, 100),
            "apiKey": self.api_key,
        }

        if category:
            params["category"] = category

        response = self.session.get(self.ENDPOINTS["top_headlines"], params=params)
        response.raise_for_status()

        data = response.json()
        if data.get("status") != "ok":
            error_msg = data.get("message", "Unknown error")
            raise RuntimeError(f"NewsAPI error: {error_msg}")

        records = []
        for article in data.get("articles", []):
            try:
                article_record = self._parse_article(article)
                records.append(article_record)
            except Exception as e:
                logger.warning(f"Error parsing article: {e}")
                continue

        if not records:
            logger.warning("No headlines found")
            return pd.DataFrame()

        return pd.DataFrame.from_records(records)
