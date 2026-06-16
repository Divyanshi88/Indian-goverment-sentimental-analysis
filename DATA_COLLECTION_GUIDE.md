# Data Collection & Model Retraining Guide

Complete workflow for collecting real-time news data and retraining your sentiment models with expanded datasets.

## Overview

Your current models are trained on only **11 samples**, which is why F1 scores are low. By collecting real news articles and labeling them, you can significantly improve model performance.

```
NewsAPI → Collect Articles → Label Sentiment → Retrain Models → Deploy
```

## Step 1: Collect Articles from NewsAPI

Fetch news articles related to government topics:

```bash
python collect_training_data.py --mode collect
```

**What this does:**
- Fetches articles from 14 government-related queries:
  - government, election, policy, parliament, prime minister, cabinet, ministry, legislation, budget, inflation, economy, development, regulation, reform
- Searches last 7 days of news
- Saves to: `data/raw/newsapi_training.csv`

**Command options:**
```bash
# Search last 3 days instead of 7
python collect_training_data.py --mode collect --days-back 3

# Get more articles per query (max 100)
python collect_training_data.py --mode collect --page-size 100

# Use custom API key
python collect_training_data.py --mode collect --api-key "your_key_here"
```

## Step 2: Label Articles with Sentiment

Open the collected articles file in Excel, Google Sheets, or any spreadsheet app:

```
data/raw/newsapi_training.csv
```

**Columns:**
- `title` - Article headline
- `description` - Article summary
- `sentiment` - **UPDATE THIS** with: `positive`, `negative`, or `neutral`
- `labeled` - **SET TO True** when done reviewing
- `notes` - Optional: add comments about labeling

**Labeling Guide:**

| Sentiment | When to Use | Examples |
|-----------|-----------|----------|
| **positive** | Article is favorable toward government/policy | "New economic policy shows promise", "Government reforms strengthen economy" |
| **negative** | Article is critical of government/policy | "Policy fails to address inflation", "Government criticized for corruption" |
| **neutral** | Informational/factual reporting | "Prime minister visits XYZ", "Budget details released", News updates without opinion |

**Quick Tips:**
1. Focus on sentiment toward government policies/actions, not just the news topic
2. If unsure, mark as `neutral`
3. Update `labeled = True` only for articles you've reviewed
4. You can label articles progressively - rerun script multiple times

## Step 3: Combine with Original Data

Combine your labeled articles with the original training data:

```bash
python collect_training_data.py --mode combine
```

**Output:** `data/processed/combined_training.csv`

This merges:
- Original training data (11 samples)
- Your newly labeled NewsAPI articles
- Creates unified dataset for retraining

## Step 4: Retrain Models

Retrain your models with the expanded dataset:

```bash
python retrain_models.py
```

**What happens:**
1. Loads combined training data
2. Only uses articles where `labeled = True`
3. Trains both Logistic Regression and Naive Bayes
4. Evaluates performance on test set
5. Saves updated models
6. Generates training history

**Expected improvements:**
- More diverse training data → better generalization
- Better F1 scores across sentiment classes
- More balanced predictions

## Step 5: Test with Real-Time Analysis

Use your improved models with real-time sentiment analysis:

```bash
python realtime_analysis.py --mode recent
```

Your updated models will now provide better sentiment predictions!

## Example Workflow

```bash
# 1. Collect articles
$ python collect_training_data.py --mode collect
✓ Collected 437 articles
✓ Saved to data/raw/newsapi_training.csv

# 2. [Open file in spreadsheet, label 50+ articles, set labeled=True]

# 3. Combine datasets
$ python collect_training_data.py --mode combine
✓ Combined dataset saved to data/processed/combined_training.csv
  Total samples: 62
  Sentiment distribution:
  positive    22
  neutral     31
  negative     9

# 4. Retrain models
$ python retrain_models.py
===============================
RETRAINING SUMMARY
===============================
Total training samples: 62
Train set: 49, Test set: 13

Logistic Regression Accuracy: 0.7692
Naive Bayes Accuracy: 0.6923

Models saved to: src/models/trained_models

# 5. Test with real data
$ python realtime_analysis.py --mode recent
[Now using improved models]
```

## Tips for Better Labeling

### 1. Start Small
- Label 20-30 articles first
- Retrain and test
- Then collect and label more

### 2. Maintain Balance
- Try to label roughly equal numbers of positive/negative/neutral
- This helps models learn each class well

### 3. Be Consistent
- Use same criteria throughout
- If you change how you define "positive", relabel affected articles

### 4. Review Difficult Cases
- If unsure, mark as `neutral`
- Focus on clear examples first

### 5. Document Your Decisions
- Use `notes` column to explain borderline cases
- Helpful for future reference and refinement

## Monitoring Progress

### Check labeled count:
```python
import pandas as pd
df = pd.read_csv("data/raw/newsapi_training.csv")
print(f"Labeled: {(df['labeled'] == True).sum()}")
print(f"Total: {len(df)}")
print(f"Progress: {100 * (df['labeled'] == True).sum() / len(df):.1f}%")
```

### View sentiment distribution:
```python
labeled = df[df['labeled'] == True]
print(labeled['sentiment'].value_counts())
```

## Automation Tips

### Collect articles periodically:
```bash
# Run weekly to keep dataset fresh
0 9 * * MON python collect_training_data.py --mode collect --days-back 7
```

### Auto-label with keyword hinting:
You could extend the script to pre-label based on keywords:
- Negative keywords: "fail", "decline", "crisis", "problem", "loss"
- Positive keywords: "growth", "success", "improve", "strong", "gain"

(Manual review still recommended)

## File Structure

```
data/
  raw/
    newsapi_training.csv          # Articles collected from NewsAPI
    reddit_posts_sample.csv       # Original data
    reddit_comments_sample.csv    # Original data
  processed/
    combined_training.csv         # Merged dataset for training
    sentiment_content.csv         # Original labeled data
src/
  models/
    trained_models/
      logistic_regression.pkl     # Updated model
      naive_bayes.pkl             # Updated model
      training_history.txt        # Retraining metrics
```

## Troubleshooting

### "NewsAPI key required"
```bash
export NEWSAPI_KEY="3416c2831f834d2fbad96773e12f953c"
python collect_training_data.py --mode collect
```

### "Not enough training data"
- Check labeled count
- Need at least 3 articles labeled to retrain
- Label more articles in `data/raw/newsapi_training.csv`

### "No articles found"
- Check internet connection
- Verify NewsAPI key is valid
- Check if quota is exceeded (100 requests/day free tier)

### Models not improving much
- Collect more articles (100+ samples)
- Improve labeling quality
- Check for class imbalance (unequal sentiment distribution)

## Next Steps

1. **Immediate:**
   - [ ] Run `collect_training_data.py --mode collect`
   - [ ] Label 30+ articles
   - [ ] Run `retrain_models.py`

2. **Short term (1-2 weeks):**
   - [ ] Collect and label 100+ articles total
   - [ ] Retrain multiple times
   - [ ] Monitor F1 scores

3. **Long term:**
   - [ ] Schedule weekly data collection
   - [ ] Set up automated labeling for high-confidence predictions
   - [ ] Consider using transformer models (BERT) for better accuracy
   - [ ] Deploy in production with improved models

## Performance Benchmarks

| Dataset Size | Expected Accuracy | Expected F1 Score |
|-------------|------------------|------------------|
| 11 (current) | ~67% | ~0.53 |
| 30-50 | ~75% | ~0.70 |
| 50-100 | ~80% | ~0.75 |
| 100+ | ~85%+ | ~0.82+ |

These are estimates - actual results depend on data quality and class balance.

## Questions?

See main README: [README.md](../README.md)
See real-time guide: [REALTIME_GUIDE.md](../REALTIME_GUIDE.md)
