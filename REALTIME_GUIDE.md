# Real-Time News Sentiment Analysis Guide

This guide explains how to use the real-time sentiment analysis features with your trained ML models using **NewsAPI.org**.

## Overview

The real-time analyzer integrates with **NewsAPI.org** to fetch live news articles, then uses your trained Logistic Regression or Naive Bayes models to classify sentiment instantly.

**Key Features:**
- Real-time news article retrieval
- Sentiment analysis on articles and headlines
- Multiple search queries support
- Both API and CLI interfaces
- CSV export for analysis results

## Setup

### 1. Get NewsAPI Key

Get your free API key from https://newsapi.org/:

1. Visit https://newsapi.org/register
2. Sign up with your email
3. Copy your API key from the dashboard
4. NewsAPI provides 100 requests/day on the free tier

### 2. Set Environment Variable

```bash
export NEWSAPI_KEY="your_api_key_here"
```

Or create a `.env` file in the project root:

```
NEWSAPI_KEY=3416c2831f834d2fbad96773e12f953c
```

**Verify your setup:**
```bash
echo $NEWSAPI_KEY
```

## Usage

### Option 1: Command-Line Script

Analyze recent news articles:

```bash
python realtime_analysis.py --mode recent
```

**Arguments:**

- `--mode`: `recent` (analyze recent articles) or `stream` (continuous updates)
- `--api-key`: NewsAPI key (if not set, reads from `NEWSAPI_KEY` env var)
- `--days-back`: Number of days back to search (default: 7)
- `--page-size`: Articles per query, max 100 (default: 100)
- `--queries`: Custom search queries (default: government-related topics)
- `--model`: ML model - `logistic_regression` or `naive_bayes` (default: `logistic_regression`)

**Examples:**

```bash
# Analyze recent news (uses default government queries)
python realtime_analysis.py --mode recent

# Search for specific topics
python realtime_analysis.py --mode recent --queries "election" "budget" "policy"

# Use Naive Bayes model
python realtime_analysis.py --mode recent --model naive_bayes

# Search 3 days back with 50 articles per query
python realtime_analysis.py --mode recent --days-back 3 --page-size 50

# Stream with custom API key
python realtime_analysis.py --mode stream --api-key your_key_here
```

### Option 2: Python API

Use the analyzer in your own Python scripts:

```python
from src.models.realtime_news_analyzer import RealtimeNewsAnalyzer
import os

# Initialize analyzer
api_key = os.getenv("NEWSAPI_KEY")
analyzer = RealtimeNewsAnalyzer(api_key=api_key, model_name="logistic_regression")

# Connect to NewsAPI
if analyzer.connect_newsapi():
    # Search and analyze articles
    df = analyzer.search_and_analyze(
        queries=["government", "election", "policy"],
        days_back=7,
        page_size=100,
    )
    
    # Get sentiment summary
    summary = analyzer.get_sentiment_summary(df)
    print(f"Total articles: {summary['total']}")
    print(f"Positive: {summary['positive']}")
    print(f"Negative: {summary['negative']}")
    print(f"Neutral: {summary['neutral']}")
    
    # Save results
    df.to_csv("analysis_results.csv", index=False)
else:
    print("Failed to connect to NewsAPI")
```

### Option 3: Using Different Analysis Methods

```python
from src.models.realtime_news_analyzer import RealtimeNewsAnalyzer
import os

analyzer = RealtimeNewsAnalyzer(api_key=os.getenv("NEWSAPI_KEY"))
analyzer.connect_newsapi()

# Method 1: Search by keywords
df1 = analyzer.search_and_analyze(
    queries=["government", "election"]
)
print("Search results:", len(df1), "articles")

# Method 2: Get top headlines (India)
df2 = analyzer.analyze_top_headlines(country="in", page_size=20)
print("Top headlines:", len(df2), "articles")

# Method 3: Combined analysis
import pandas as pd
combined = pd.concat([df1, df2])
summary = analyzer.get_sentiment_summary(combined)
print("Combined analysis:", summary)
```

## Output Format

Analysis results are returned as a DataFrame with these columns:

- `article_id` - Unique article identifier
- `source_name` - News source (e.g., "BBC", "CNN India")
- `title` - Article headline
- `description` - Article summary
- `content` - Article content (first 200 chars)
- `clean_text` - Preprocessed text
- `sentiment` - Predicted sentiment (`POSITIVE`, `NEGATIVE`, or `NEUTRAL`)
- `sentiment_probability` - Confidence score (0-1)
- `author` - Article author
- `published_at` - Publication timestamp
- `url` - Full article URL
- `image_url` - Article image URL
- `sentiment_keywords` - Keywords/queries used to find this article

## Examples

### Example 1: Analyze Government-Related News

```python
from src.models.realtime_news_analyzer import RealtimeNewsAnalyzer
import os

analyzer = RealtimeNewsAnalyzer(api_key=os.getenv("NEWSAPI_KEY"))
analyzer.connect_newsapi()

# Search government-related news
queries = ["government", "parliament", "prime minister", "cabinet", "ministry"]
df = analyzer.search_and_analyze(queries=queries, days_back=7)

# Show sentiment distribution
summary = analyzer.get_sentiment_summary(df)
print(f"Total articles: {summary['total']}")
print(f"Sentiment distribution: {summary['distribution']}")

# Find negative articles
negative = df[df['sentiment'] == 'NEGATIVE']
print(f"\nNegative articles ({len(negative)}):")
for _, row in negative.head(5).iterrows():
    print(f"  - {row['title']}")
    print(f"    Source: {row['source_name']}")
    print(f"    Prob: {row['sentiment_probability']:.3f}\n")
```

### Example 2: Compare Sentiment Across Models

```python
from src.models.realtime_news_analyzer import RealtimeNewsAnalyzer
import os

api_key = os.getenv("NEWSAPI_KEY")

for model_name in ["logistic_regression", "naive_bayes"]:
    analyzer = RealtimeNewsAnalyzer(api_key=api_key, model_name=model_name)
    analyzer.connect_newsapi()
    
    df = analyzer.search_and_analyze(["election"], days_back=3)
    summary = analyzer.get_sentiment_summary(df)
    
    print(f"\n{model_name.upper()}:")
    print(f"  Positive: {summary['positive']}/{summary['total']}")
    print(f"  Negative: {summary['negative']}/{summary['total']}")
    print(f"  Neutral: {summary['neutral']}/{summary['total']}")
```

### Example 3: Top Headlines Analysis

```python
from src.models.realtime_news_analyzer import RealtimeNewsAnalyzer
import os

analyzer = RealtimeNewsAnalyzer(api_key=os.getenv("NEWSAPI_KEY"))
analyzer.connect_newsapi()

# Get and analyze top headlines for India
df = analyzer.analyze_top_headlines(country="in", page_size=20)
summary = analyzer.get_sentiment_summary(df)

print(f"Top Headlines Summary:")
print(f"  Total: {summary['total']}")
print(f"  Positive: {summary['positive']} ({100*summary['positive']/summary['total']:.1f}%)")
print(f"  Negative: {summary['negative']} ({100*summary['negative']/summary['total']:.1f}%)")
print(f"  Neutral: {summary['neutral']} ({100*summary['neutral']/summary['total']:.1f}%)")
```

## Troubleshooting

### 1. "NewsAPI key not found" Error

**Issue:** API key not set or not found

**Solution:**
```bash
# Set environment variable
export NEWSAPI_KEY="your_key_here"

# Or verify it's set
echo $NEWSAPI_KEY
```

### 2. "NewsAPI error: Your API key is invalid" Error

**Issue:** API key is incorrect or expired

**Solution:**
1. Check your key at https://newsapi.org/account/api-keys
2. Regenerate the key if needed
3. Update the environment variable

### 3. "No articles found" Warning

**Issue:** Search query doesn't match any articles

**Solution:**
- Try broader search terms
- Increase `days_back` parameter
- Check if the article exists on NewsAPI website

### 4. Rate Limiting (429 Error)

**Issue:** Exceeded API quota (100 requests/day on free tier)

**Solution:**
- Upgrade to paid plan at https://newsapi.org/pricing
- Wait until next day for free tier quota reset
- Reduce number of queries

### 5. "Models not found" Error

**Issue:** Trained ML models haven't been generated

**Solution:**
```bash
python train_models.py
```

## Performance Notes

- **Dataset Size:** Models trained on limited samples - accuracy improves with more training data
- **Speed:** ~100-200ms per article for sentiment analysis
- **API Calls:** NewsAPI free tier: 100 requests/day
- **Accuracy:** ~67-75% on validation set
- **Latency:** Results returned in 1-5 seconds depending on article count

## Comparison: NewsAPI vs Reddit

| Aspect | NewsAPI | Reddit (Legacy) |
|--------|---------|-----------------|
| **Cost** | Free (100/day) → Paid | Free (deprecated) |
| **Data Source** | Professional news outlets | User-generated content |
| **Bias** | Lower (news outlets) | Higher (user opinions) |
| **Volume** | 200k+ articles daily | Unlimited |
| **API Stability** | Very stable | Stable |
| **Setup** | Simple (1 key) | Complex (3 credentials) |

## Next Steps

1. **Increase Accuracy:** Train models on more labeled news articles
2. **Custom Queries:** Add domain-specific search terms
3. **Real-Time Alerts:** Set up notifications for sentiment changes
4. **Database Integration:** Store results in BigQuery for analysis
5. **Dashboard:** Deploy Streamlit dashboard with news updates
6. **Scheduled Jobs:** Run analysis on a schedule via cron/Cloud Scheduler

## API Reference

### RealtimeNewsAnalyzer Class

```python
class RealtimeNewsAnalyzer:
    def __init__(
        self, 
        api_key: Optional[str] = None,
        model_name: str = "logistic_regression"
    )
    
    def connect_newsapi(self) -> bool
    
    def analyze_article(
        self,
        article: dict,
        sentiment_keywords: Optional[list[str]] = None,
    ) -> dict
    
    def analyze_articles(self, articles_df: pd.DataFrame) -> pd.DataFrame
    
    def search_and_analyze(
        self,
        queries: list[str],
        days_back: int = 7,
        page_size: int = 100,
        sort_by: str = "publishedAt",
    ) -> pd.DataFrame
    
    def analyze_top_headlines(
        self,
        country: str = "in",
        page_size: int = 20,
    ) -> pd.DataFrame
    
    def get_sentiment_summary(self, articles_df: pd.DataFrame) -> dict
```

### NewsAPIClient Class

```python
class NewsAPIClient:
    def __init__(self, api_key: str)
    
    def search_articles(
        self,
        queries: Iterable[str],
        language: str = "en",
        sort_by: str = "publishedAt",
        page_size: int = 100,
        days_back: int = 7,
    ) -> pd.DataFrame
    
    def get_top_headlines(
        self,
        country: str = "in",
        category: Optional[str] = None,
        page_size: int = 20,
    ) -> pd.DataFrame
```

## Resources

- **NewsAPI Docs:** https://newsapi.org/docs
- **Free API Key:** https://newsapi.org/register
- **API Status:** https://newsapi.org/sources
- **Python Requests:** https://requests.readthedocs.io/

