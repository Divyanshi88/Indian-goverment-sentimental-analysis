"""Offline sample data for demos, tests, and first-run dashboards."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

SAMPLE_POSTS = [
    {
        "post_id": "p001",
        "subreddit": "india",
        "title": "New infrastructure project announced for rail corridors",
        "selftext": "People are hopeful about jobs but worried about land acquisition delays.",
        "score": 840,
        "author": "policywatcher",
        "created_utc": "2026-05-20T09:30:00+00:00",
        "num_comments": 152,
        "url": "https://reddit.com/r/india/example1",
        "permalink": "https://reddit.com/r/india/comments/p001",
    },
    {
        "post_id": "p002",
        "subreddit": "IndiaSpeaks",
        "title": "Budget discussion: tax relief for middle class",
        "selftext": "Many users welcomed the change, though some said inflation remains painful.",
        "score": 1260,
        "author": "econthread",
        "created_utc": "2026-05-21T13:45:00+00:00",
        "num_comments": 321,
        "url": "https://reddit.com/r/IndiaSpeaks/example2",
        "permalink": "https://reddit.com/r/IndiaSpeaks/comments/p002",
    },
    {
        "post_id": "p003",
        "subreddit": "unitedstatesofindia",
        "title": "Debate over data privacy bill intensifies",
        "selftext": "Critics argue the bill needs stronger safeguards and independent oversight.",
        "score": 690,
        "author": "civicsnerd",
        "created_utc": "2026-05-22T18:10:00+00:00",
        "num_comments": 244,
        "url": "https://reddit.com/r/unitedstatesofindia/example3",
        "permalink": "https://reddit.com/r/unitedstatesofindia/comments/p003",
    },
    {
        "post_id": "p004",
        "subreddit": "indianews",
        "title": "Healthcare scheme expands to additional districts",
        "selftext": "Beneficiaries praised access improvements, but doctors flagged staffing shortages.",
        "score": 510,
        "author": "newsdesk",
        "created_utc": "2026-05-23T07:25:00+00:00",
        "num_comments": 87,
        "url": "https://reddit.com/r/indianews/example4",
        "permalink": "https://reddit.com/r/indianews/comments/p004",
    },
    {
        "post_id": "p005",
        "subreddit": "india",
        "title": "Students protest exam portal glitches",
        "selftext": "Applicants described the rollout as frustrating and demanded accountability.",
        "score": 970,
        "author": "studentvoice",
        "created_utc": "2026-05-24T11:05:00+00:00",
        "num_comments": 198,
        "url": "https://reddit.com/r/india/example5",
        "permalink": "https://reddit.com/r/india/comments/p005",
    },
]

SAMPLE_COMMENTS = [
    {
        "comment_id": "c001",
        "post_id": "p001",
        "subreddit": "india",
        "body": "Rail upgrades are badly needed and this could create local jobs.",
        "score": 94,
        "author": "infraoptimist",
        "created_utc": "2026-05-20T10:05:00+00:00",
        "permalink": "https://reddit.com/r/india/comments/p001/c001",
    },
    {
        "comment_id": "c002",
        "post_id": "p001",
        "subreddit": "india",
        "body": "Announcements are easy. Execution delays are the real issue.",
        "score": 121,
        "author": "skeptic_delhi",
        "created_utc": "2026-05-20T10:20:00+00:00",
        "permalink": "https://reddit.com/r/india/comments/p001/c002",
    },
    {
        "comment_id": "c003",
        "post_id": "p002",
        "subreddit": "IndiaSpeaks",
        "body": "Tax relief is welcome, finally something tangible for salaried people.",
        "score": 210,
        "author": "salaryslip",
        "created_utc": "2026-05-21T14:10:00+00:00",
        "permalink": "https://reddit.com/r/IndiaSpeaks/comments/p002/c003",
    },
    {
        "comment_id": "c004",
        "post_id": "p003",
        "subreddit": "unitedstatesofindia",
        "body": "Privacy protections are still weak. Oversight should not be optional.",
        "score": 187,
        "author": "rightsfirst",
        "created_utc": "2026-05-22T19:00:00+00:00",
        "permalink": "https://reddit.com/r/unitedstatesofindia/comments/p003/c004",
    },
    {
        "comment_id": "c005",
        "post_id": "p004",
        "subreddit": "indianews",
        "body": "Good expansion, but hospitals need staff and medicine supply too.",
        "score": 63,
        "author": "publichealth",
        "created_utc": "2026-05-23T08:45:00+00:00",
        "permalink": "https://reddit.com/r/indianews/comments/p004/c005",
    },
    {
        "comment_id": "c006",
        "post_id": "p005",
        "subreddit": "india",
        "body": "The portal failure was unacceptable. Students deserve better planning.",
        "score": 154,
        "author": "examuser",
        "created_utc": "2026-05-24T12:15:00+00:00",
        "permalink": "https://reddit.com/r/india/comments/p005/c006",
    },
]


def write_sample_data(data_dir: Path) -> tuple[Path, Path]:
    """Write sample posts and comments to disk."""
    raw_dir = data_dir / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)
    posts_path = raw_dir / "reddit_posts_sample.csv"
    comments_path = raw_dir / "reddit_comments_sample.csv"
    pd.DataFrame(SAMPLE_POSTS).to_csv(posts_path, index=False)
    pd.DataFrame(SAMPLE_COMMENTS).to_csv(comments_path, index=False)
    return posts_path, comments_path
