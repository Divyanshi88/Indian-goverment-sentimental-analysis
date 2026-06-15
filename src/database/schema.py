"""Database schema definitions."""

RAW_POSTS_SCHEMA = [
    {"name": "post_id", "type": "STRING", "mode": "REQUIRED"},
    {"name": "subreddit", "type": "STRING", "mode": "NULLABLE"},
    {"name": "title", "type": "STRING", "mode": "NULLABLE"},
    {"name": "selftext", "type": "STRING", "mode": "NULLABLE"},
    {"name": "score", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "author", "type": "STRING", "mode": "NULLABLE"},
    {"name": "created_utc", "type": "TIMESTAMP", "mode": "NULLABLE"},
    {"name": "num_comments", "type": "INTEGER", "mode": "NULLABLE"},
    {"name": "url", "type": "STRING", "mode": "NULLABLE"},
    {"name": "permalink", "type": "STRING", "mode": "NULLABLE"},
]

PROCESSED_CONTENT_SCHEMA = [
    {"name": "content_id", "type": "STRING", "mode": "NULLABLE"},
    {"name": "post_id", "type": "STRING", "mode": "NULLABLE"},
    {"name": "content_type", "type": "STRING", "mode": "NULLABLE"},
    {"name": "subreddit", "type": "STRING", "mode": "NULLABLE"},
    {"name": "clean_text", "type": "STRING", "mode": "NULLABLE"},
    {"name": "sentiment", "type": "STRING", "mode": "NULLABLE"},
    {"name": "sentiment_probability", "type": "FLOAT", "mode": "NULLABLE"},
    {"name": "topic_label", "type": "STRING", "mode": "NULLABLE"},
    {"name": "created_utc", "type": "TIMESTAMP", "mode": "NULLABLE"},
]
