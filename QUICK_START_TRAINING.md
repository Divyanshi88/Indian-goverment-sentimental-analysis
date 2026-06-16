# 🚀 Your Complete Data Training Workflow

## Current Status ✅

✅ **684 articles collected** from NewsAPI  
✅ **Ready for labeling and retraining**  

```
YOUR WORKFLOW:
  
  1. Collect Articles (✓ DONE - 684 articles)
         ↓
  2. Label Sentiment (← YOU ARE HERE)
         ↓
  3. Combine Datasets
         ↓
  4. Retrain Models
         ↓
  5. Deploy & Test
```

---

## Step 1: Label Your Articles

You have **684 articles** saved at:
```
data/raw/newsapi_training.csv
```

### Option A: Manual Labeling (Best Quality)

1. **Open the file in Excel/Google Sheets/CSV editor**
2. **Review each article** and update the `sentiment` column:
   - `positive` - Positive toward government/policies
   - `negative` - Critical of government/policies  
   - `neutral` - Factual/informational
3. **Set `labeled = True`** when done reviewing
4. **Save the file**

**Example:**

| title | sentiment | labeled |
|-------|-----------|---------|
| "India's Economy Shows Growth" | positive | True |
| "Government Announces Reforms" | positive | True |
| "Budget Details Released" | neutral | True |
| "Economic Crisis Worsens" | negative | True |

### Option B: Hybrid Approach (Faster)

1. Use auto-labeling to get suggestions:
   ```bash
   python label_articles.py --mode predict
   ```
2. Review and correct the auto-labeled articles
3. Manually label articles the script missed
4. Set `labeled = True` when done

### Option C: Start with Sample Data (For Testing)

To understand the workflow quickly, we created sample labeled data:

```bash
python label_articles.py --mode sample
```

This creates `data/raw/sample_labeled.csv` with 9 pre-labeled examples.

---

## Quick Start: Using Sample Data

### Test the full workflow immediately:

```bash
# 1. Create sample labeled data (9 articles)
python label_articles.py --mode sample

# 2. Combine sample with original data
python collect_training_data.py --mode combine

# 3. Retrain models
python retrain_models.py
```

This will:
- Use the 9 sample labeled articles
- Keep your original 11 samples
- Create 20 total training samples
- Show improved F1 scores

---

## Then: Scale Up with Your 684 Articles

Once you understand the workflow, label more articles:

```bash
# 1. Label articles in data/raw/newsapi_training.csv
# [Open file, update sentiment & labeled columns]

# 2. Combine all data
python collect_training_data.py --mode combine

# 3. Retrain with full dataset
python retrain_models.py
```

**Expected results with 100+ labeled articles:**
- Accuracy: 80%+
- F1 Score: 0.75+
- Better sentiment predictions

---

## Quick Reference: Commands

### **Collect Articles**
```bash
# Collect fresh articles (updates data/raw/newsapi_training.csv)
python collect_training_data.py --mode collect
```

### **Label Articles**
```bash
# Create sample for testing
python label_articles.py --mode sample

# Auto-label your articles (creates suggestions)
python label_articles.py --mode predict --confidence 0.5
```

### **Combine Data**
```bash
# Merge labeled articles with original training data
python collect_training_data.py --mode combine
```

### **Retrain Models**
```bash
# Train with combined dataset
python retrain_models.py
```

### **Test Results**
```bash
# Use improved models for real-time sentiment analysis
python realtime_analysis.py --mode recent
```

---

## File Structure

```
data/
  raw/
    newsapi_training.csv              ← 684 articles (ready to label)
    newsapi_training_prelabeled.csv   ← Auto-labeled suggestions
    sample_labeled.csv                ← 9 examples for testing
  processed/
    combined_training.csv             ← Merged dataset for training
    
src/models/trained_models/
  logistic_regression.pkl             ← Updated model
  naive_bayes.pkl                     ← Updated model
  training_history.txt                ← Performance metrics
```

---

## Expected Performance Improvements

| Stage | Accuracy | F1 Score | Notes |
|-------|----------|----------|-------|
| **Current** | 66.7% | 0.53 | 11 samples |
| **After Sample** | ~75% | ~0.70 | 20 samples |
| **After 50 Labels** | ~78% | ~0.72 | 61 samples |
| **After 100 Labels** | ~82% | ~0.77 | 111 samples |
| **After 200+ Labels** | ~85%+ | ~0.82+ | 211+ samples |

---

## 🎯 Recommended Next Steps

### **Quick Test (30 minutes):**
```bash
# 1. Create sample data and test workflow
python label_articles.py --mode sample
python collect_training_data.py --mode combine
python retrain_models.py

# 2. See improved results
python realtime_analysis.py --mode recent
```

### **Build Real Model (2-3 hours):**
```bash
# 1. Label 50-100 articles from your 684
# 2. Run retraining pipeline:
python collect_training_data.py --mode combine
python retrain_models.py

# 3. Deploy improved models
```

### **Production Quality (1-2 days):**
```bash
# 1. Label 200+ articles systematically
# 2. Maintain data quality
# 3. Retrain weekly with new articles
# 4. Monitor F1 scores
```

---

## Tools Provided

### **collect_training_data.py**
- Fetch articles from NewsAPI
- Combine datasets
- Usage: `python collect_training_data.py [--mode collect|combine]`

### **label_articles.py**
- Auto-label with keywords
- Create sample data
- Usage: `python label_articles.py [--mode predict|sample]`

### **retrain_models.py**
- Retrain with new data
- Generate metrics
- Usage: `python retrain_models.py`

### **realtime_analysis.py** (existing)
- Test models on real data
- Usage: `python realtime_analysis.py --mode recent`

---

## Tips for Success

✅ **Do:**
- Start with sample data to understand workflow
- Label articles consistently
- Maintain balance (some positive, negative, neutral)
- Retrain after labeling 20-50 articles
- Save frequently

❌ **Don't:**
- Label all 684 at once (too much at once)
- Rush through labeling (quality matters)
- Forget to set `labeled = True`
- Ignore underrepresented sentiment classes
- Manual labor: there's the sample data to learn!

---

## FAQ

**Q: How many articles do I need to label?**  
A: Start with 20-50 for meaningful improvement. Aim for 100+ for good models.

**Q: How long does labeling take?**  
A: ~1-2 minutes per article. 50 articles = 1-2 hours.

**Q: Can I label articles partially?**  
A: Yes! Label some, retrain, then label more. The pipeline is iterative.

**Q: What if I make mistakes in labeling?**  
A: It's okay. Just re-label and retrain. Start fresh anytime.

**Q: Which model is better?**  
A: Usually similar performance. Compare in retraining output. Use your preference.

**Q: Can I automate labeling completely?**  
A: Not recommended. Manual review ensures quality. Auto-suggestions help speed up.

---

## Troubleshooting

**Error: "Not enough training data"**
- Make sure `labeled = True` in your CSV
- Need at least 3 labeled articles

**Error: "NewsAPI key required"**
```bash
export NEWSAPI_KEY="3416c2831f834d2fbad96773e12f953c"
python collect_training_data.py --mode collect
```

**Models not improving**
- Label more diverse articles
- Check sentiment balance
- Make sure labeling is accurate
- Try labeling 50+ articles minimum

**Can't find CSV files**
- Verify file paths exist
- Check: `ls data/raw/newsapi_training.csv`
- Check: `ls data/processed/`

---

## Resources

- [Data Collection Guide](DATA_COLLECTION_GUIDE.md) - Detailed workflow
- [Real-Time Guide](REALTIME_GUIDE.md) - Testing models
- [README](README.md) - Project overview

---

## Summary

You now have:
1. ✅ **684 articles** collected and ready
2. ✅ **Scripts** to label, combine, and retrain
3. ✅ **Sample data** for testing the workflow
4. ✅ **Complete pipeline** to improve models

**Next action:** Choose your path!

```
🟢 QUICK TEST (30 min)
   python label_articles.py --mode sample
   
🟡 REAL MODEL (2-3 hours)
   [Label 50-100 articles]
   python retrain_models.py
   
🔴 PRODUCTION (1-2 days)
   [Label 200+ articles]
   [Retrain & monitor]
```

Go build great models! 🚀
