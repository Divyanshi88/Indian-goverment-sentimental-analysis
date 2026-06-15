"""Reddit ingestion using PRAW."""

from __future__ import annotations

import os
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from typing import Iterable

import pandas as pd
import praw

from src.utils.logging import get_logger

logger = get_logger(__name__)


@dataclass(frozen=True)
class RedditPost:
    post_id: str
    subreddit: str
    title: str
    selftext: str
    score: int
    author: str
    created_utc: str
    num_comments: int
    url: str
    permalink: str


@dataclass(frozen=True)
class RedditComment:
    comment_id: str
    post_id: str
    subreddit: str
    body: str
    score: int
    author: str
    created_utc: str
    permalink: str


def create_reddit_client() -> praw.Reddit:
    """Create an authenticated PRAW client from environment variables."""
    required = ["REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET", "REDDIT_USER_AGENT"]
    missing = [name for name in required if not os.getenv(name)]
    if missing:
        raise RuntimeError(f"Missing Reddit credentials: {', '.join(missing)}")

    return praw.Reddit(
        client_id=os.environ["REDDIT_CLIENT_ID"],
        client_secret=os.environ["REDDIT_CLIENT_SECRET"],
        user_agent=os.environ["REDDIT_USER_AGENT"],
    )


def _utc_string(timestamp: float) -> str:
    return datetime.fromtimestamp(timestamp, tz=UTC).isoformat()


def collect_posts(
    reddit: praw.Reddit,
    subreddits: Iterable[str],
    limit: int = 100,
) -> pd.DataFrame:
    """Collect hot posts from configured subreddits."""
    records: list[dict[str, object]] = []
    for subreddit_name in subreddits:
        logger.info("Collecting posts from r/%s", subreddit_name)
        subreddit = reddit.subreddit(subreddit_name)
        for post in subreddit.hot(limit=limit):
            records.append(
                asdict(
                    RedditPost(
                        post_id=post.id,
                        subreddit=subreddit_name,
                        title=post.title or "",
                        selftext=post.selftext or "",
                        score=int(post.score),
                        author=str(post.author) if post.author else "[deleted]",
                        created_utc=_utc_string(post.created_utc),
                        num_comments=int(post.num_comments),
                        url=post.url,
                        permalink=f"https://reddit.com{post.permalink}",
                    )
                )
            )
    return pd.DataFrame.from_records(records)


def collect_comments(
    reddit: praw.Reddit,
    post_ids: Iterable[str],
    comment_limit: int = 50,
) -> pd.DataFrame:
    """Collect top-level comments for a set of Reddit submissions."""
    records: list[dict[str, object]] = []
    for post_id in post_ids:
        submission = reddit.submission(id=post_id)
        submission.comments.replace_more(limit=0)
        for comment in list(submission.comments)[:comment_limit]:
            records.append(
                asdict(
                    RedditComment(
                        comment_id=comment.id,
                        post_id=post_id,
                        subreddit=str(submission.subreddit),
                        body=comment.body or "",
                        score=int(comment.score),
                        author=str(comment.author) if comment.author else "[deleted]",
                        created_utc=_utc_string(comment.created_utc),
                        permalink=f"https://reddit.com{comment.permalink}",
                    )
                )
            )
    return pd.DataFrame.from_records(records)
