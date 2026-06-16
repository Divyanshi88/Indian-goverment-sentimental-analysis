# NewsAPI Setup Guide

Quick setup guide for using NewsAPI.org with this project.

## Step 1: Get Your Free API Key

1. Visit https://newsapi.org/register
2. Sign up with your email (free account)
3. Verify your email
4. Copy your API key from the dashboard
5. Free tier provides 100 requests/day

**Your API Key:**
```
3416c2831f834d2fbad96773e12f953c
```

## Step 2: Set Environment Variable

### Option A: Export in Terminal (Temporary)
```bash
export NEWSAPI_KEY="3416c2831f834d2fbad96773e12f953c"
```

### Option B: Create .env File (Permanent)
Create a `.env` file in the project root:

```bash
# .env
NEWSAPI_KEY=3416c2831f834d2fbad96773e12f953c
```

Then source it before running:
```bash
source .env
```

### Option C: Pass as Command-Line Argument
```bash
python realtime_analysis.py --api-key "3416c2831f834d2fbad96773e12f953c"
```

## Step 3: Verify Setup

```bash
# Check environment variable is set
echo $NEWSAPI_KEY

# Run a test analysis
python realtime_analysis.py --mode recent
```

You should see output like:
```
=====================================================
REAL-TIME NEWS SENTIMENT ANALYSIS
=====================================================

======================================================
SEARCHING FOR ARTICLES
...
```

## API Limits

| Plan | Requests/Day | Sources | History |
|------|-------------|---------|---------|
| Free | 100 | 38 | 1 month |
| Developer | 500 | All | 1 month |
| Business | 10,000+ | All | Unlimited |

**Current:** Free tier (100 requests/day)

## Usage Examples

### Basic Analysis (Default Queries)
```bash
python realtime_analysis.py --mode recent
```

### Custom Search
```bash
python realtime_analysis.py --mode recent --queries "election" "budget" "parliament"
```

### Different Time Period
```bash
python realtime_analysis.py --mode recent --days-back 3
```

### More Articles Per Query
```bash
python realtime_analysis.py --mode recent --page-size 100
```

### Use Naive Bayes Model
```bash
python realtime_analysis.py --mode recent --model naive_bayes
```

## Python API Usage

```python
import os
from src.models.realtime_news_analyzer import RealtimeNewsAnalyzer

# Initialize
api_key = os.getenv("NEWSAPI_KEY")
analyzer = RealtimeNewsAnalyzer(api_key=api_key)

# Connect
if analyzer.connect_newsapi():
    # Search articles
    df = analyzer.search_and_analyze(
        queries=["government", "election"],
        days_back=7
    )
    
    # Get summary
    summary = analyzer.get_sentiment_summary(df)
    print(f"Total articles: {summary['total']}")
    print(f"Positive: {summary['positive']}")
    print(f"Negative: {summary['negative']}")
    
    # Save results
    df.to_csv("results.csv", index=False)
```

## Troubleshooting

### "Invalid API key"
- Check key is correct: `echo $NEWSAPI_KEY`
- Verify at https://newsapi.org/account/api-keys
- Try regenerating the key

### "429 Too Many Requests"
- Free tier limit: 100 requests/day
- Upgrade plan: https://newsapi.org/pricing
- Or wait until next day for quota reset

### "No articles found"
- Try different keywords
- Increase `--days-back` value
- Check if articles exist on https://newsapi.org/

## Free Tier Details

**Included Sources (38):**
- BBC, CNN, Reuters, Associated Press
- Business Insider, Financial Times
- Wired, TechCrunch, The Next Web
- And 29+ more

**Available in India:** Yes, with country=in filter

**Historical Data:** Last 30 days

## Upgrade Options

If you need more requests:

1. **Developer Plan** - $25/month for 500 requests/day
2. **Business Plan** - Custom pricing for 10,000+ requests/day

Visit: https://newsapi.org/pricing

## Documentation

- NewsAPI Docs: https://newsapi.org/docs
- Real-Time Guide: [REALTIME_GUIDE.md](../REALTIME_GUIDE.md)
- Python Requests: https://requests.readthedocs.io/

## Next Steps

1. ✅ Set up NEWSAPI_KEY
2. Run: `python realtime_analysis.py --mode recent`
3. Check output files: `realtime_articles_analysis.csv`, `realtime_headlines_analysis.csv`
4. Train models: `python train_models.py`
5. View dashboard: `streamlit run dashboard/app.py`
