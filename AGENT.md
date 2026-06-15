# AGENT.md

## Project Name

Indian Government Sentiment Analysis Dashboard

---

## Project Overview

You are an expert Senior Data Scientist, Machine Learning Engineer, Data Engineer, and Full-Stack Developer working on a production-quality portfolio project.

Your task is to build a complete end-to-end data science system that collects Reddit discussions related to the Indian government, performs sentiment analysis using machine learning models, stores processed data in a cloud database, and presents insights through an interactive web dashboard.

The final project should look professional enough to showcase on GitHub, LinkedIn, and during Data Science job interviews.

---

# Business Problem

Public opinion about government policies changes continuously.

Government agencies, journalists, researchers, and analysts often need a way to understand:

* What people are discussing
* Whether sentiment is positive, negative, or neutral
* How sentiment changes over time
* Which topics generate the strongest reactions

This project aims to build a real-time sentiment monitoring platform using Reddit discussions.

---

# Project Objectives

Build an end-to-end machine learning pipeline that:

1. Collects Reddit posts and comments.
2. Cleans and preprocesses text data.
3. Performs sentiment analysis.
4. Compares multiple ML models.
5. Stores data in a cloud database.
6. Displays insights in an interactive dashboard.
7. Supports future real-time deployment.

---

# Data Source

Use Reddit API via PRAW.

Target subreddits:

* r/india
* r/IndiaSpeaks
* r/indianews
* r/unitedstatesofindia
* Additional India-related political/news subreddits if useful

Collect:

### Posts

* Title
* Self text
* Score
* Author
* Created date
* Number of comments
* URL

### Comments

* Comment body
* Score
* Author
* Created date
* Parent post ID

---

# Machine Learning Goals

Implement multiple sentiment analysis approaches.

## Baseline Model

Logistic Regression

Requirements:

* TF-IDF Vectorization
* Train/Test Split
* Accuracy
* Precision
* Recall
* F1 Score
* Confusion Matrix

---

## Traditional Model Comparison

Implement:

* Naive Bayes
* Logistic Regression

Compare:

* Accuracy
* Precision
* Recall
* F1 Score

---

## Advanced Model

Implement transformer-based sentiment analysis using:

* BERT
* DistilBERT

Use HuggingFace Transformers.

Compare performance against traditional ML models.

---

# Data Processing Requirements

Create reusable preprocessing pipelines.

Steps:

1. Lowercase conversion
2. URL removal
3. HTML removal
4. Punctuation removal
5. Number removal
6. Emoji handling
7. Stopword removal
8. Lemmatization
9. Duplicate removal
10. Missing value handling

Use:

* pandas
* nltk
* spacy

---

# Topic Analysis

Implement:

## Keyword Extraction

Using:

* TF-IDF
* KeyBERT

## Topic Modeling

Using:

* LDA

Output:

* Top topics
* Topic keywords
* Topic trends over time

---

# Cloud Database

Choose one of the following:

Preferred:

* Google BigQuery

Alternative:

* Google Firestore
* AWS RDS
* AWS DynamoDB

Store:

### Raw Data

* Reddit posts
* Reddit comments

### Processed Data

* Clean text
* Sentiment labels
* Prediction probabilities
* Topic labels

### Aggregated Analytics

* Daily sentiment counts
* Weekly sentiment trends
* Trending keywords

Database design should be scalable.

---

# Dashboard Requirements

Use Streamlit.

Dashboard must be modern, responsive, and recruiter-friendly.

Create the following pages:

## 1. Overview Page

Display:

* Total posts analyzed
* Total comments analyzed
* Positive %
* Negative %
* Neutral %

Use KPI cards.

---

## 2. Sentiment Distribution

Visualizations:

* Pie chart
* Bar chart

Libraries:

* Plotly
* Altair

---

## 3. Sentiment Timeline

Show:

* Daily trend
* Weekly trend
* Monthly trend

Interactive date filters required.

---

## 4. Word Cloud Analysis

Separate word clouds for:

* Positive sentiment
* Negative sentiment

Use:

* wordcloud library

---

## 5. Trending Topics

Display:

* Top keywords
* Topic clusters
* Topic frequency

---

## 6. Reddit Post Explorer

Search and filter:

* Subreddit
* Date range
* Sentiment
* Keywords

Display original post text.

---

# Deployment Requirements

Deploy dashboard using one of:

* Streamlit Cloud
* Render
* Railway

Deployment should include:

* Environment variables
* Secret management
* Requirements.txt
* Docker support

---

# Project Architecture

Follow clean architecture principles.

Expected structure:

project-root/

├── data/
│   ├── raw/
│   ├── processed/
│   └── external/
│
├── notebooks/
│
├── src/
│   ├── data_collection/
│   ├── preprocessing/
│   ├── feature_engineering/
│   ├── models/
│   ├── database/
│   ├── analytics/
│   └── utils/
│
├── dashboard/
│   ├── pages/
│   ├── components/
│   └── assets/
│
├── deployment/
│
├── tests/
│
├── config/
│
├── models/
│
├── requirements.txt
├── README.md
├── .env.example
└── main.py

---

# Coding Standards

Follow:

* PEP8
* Type hints
* Modular functions
* Docstrings
* Logging
* Error handling

Avoid:

* Hardcoded credentials
* Monolithic scripts
* Repeated code

---

# Deliverables

Generate:

1. Complete folder structure.
2. Production-ready Python code.
3. Database schema.
4. ML training pipelines.
5. Evaluation reports.
6. Streamlit dashboard.
7. Deployment files.
8. Docker configuration.
9. GitHub-ready README.
10. Architecture diagrams (Mermaid).

---

# Success Criteria

The project should demonstrate:

* Data Collection
* Data Engineering
* NLP
* Machine Learning
* Cloud Integration
* Dashboard Development
* Deployment Skills

This project must be portfolio-quality and strong enough to be discussed during Data Science, Machine Learning Engineer, or Data Analyst interviews.
