CREATE SCHEMA IF NOT EXISTS `reddit_government_sentiment`;

CREATE TABLE IF NOT EXISTS `reddit_government_sentiment.raw_posts` (
  post_id STRING NOT NULL,
  subreddit STRING,
  title STRING,
  selftext STRING,
  score INT64,
  author STRING,
  created_utc TIMESTAMP,
  num_comments INT64,
  url STRING,
  permalink STRING
);

CREATE TABLE IF NOT EXISTS `reddit_government_sentiment.raw_comments` (
  comment_id STRING NOT NULL,
  post_id STRING,
  subreddit STRING,
  body STRING,
  score INT64,
  author STRING,
  created_utc TIMESTAMP,
  permalink STRING
);

CREATE TABLE IF NOT EXISTS `reddit_government_sentiment.processed_content` (
  content_id STRING,
  post_id STRING,
  content_type STRING,
  subreddit STRING,
  clean_text STRING,
  sentiment STRING,
  sentiment_probability FLOAT64,
  topic_label STRING,
  created_utc TIMESTAMP
);

CREATE TABLE IF NOT EXISTS `reddit_government_sentiment.daily_sentiment_counts` (
  period DATE,
  subreddit STRING,
  sentiment STRING,
  count INT64
);
