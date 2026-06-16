"""Script to train sentiment classification models."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.data_collection.sample_data import write_sample_data
from src.models.sentiment import add_sentiment_labels
from src.models.train_models import SentimentModelTrainer
from src.preprocessing.text_cleaner import preprocess_comments, preprocess_posts
from src.utils.config import ROOT_DIR
from src.utils.logging import get_logger

logger = get_logger(__name__)


def train_sentiment_models() -> None:
    """Train sentiment classification models on sample data."""
    # Prepare data
    logger.info("=" * 60)
    logger.info("SENTIMENT MODEL TRAINING PIPELINE")
    logger.info("=" * 60)

    posts_path, comments_path = write_sample_data(ROOT_DIR / "data")
    logger.info(f"Loaded sample data from {posts_path} and {comments_path}")

    # Preprocess data
    posts = add_sentiment_labels(preprocess_posts(pd.read_csv(posts_path)))
    comments = add_sentiment_labels(preprocess_comments(pd.read_csv(comments_path)))

    # Combine posts and comments for training
    combined_data = pd.concat([posts, comments], ignore_index=True)
    logger.info(f"Combined dataset has {len(combined_data)} samples")
    logger.info(f"Sentiment distribution:\n{combined_data['sentiment'].value_counts()}")

    # Initialize trainer
    model_dir = ROOT_DIR / "src" / "models" / "trained_models"
    trainer = SentimentModelTrainer(model_dir=model_dir)

    # Prepare training data
    X_train, X_test, y_train, y_test = trainer.prepare_data(
        combined_data, text_column="clean_text", label_column="sentiment"
    )

    # Train models
    logger.info("\n" + "=" * 60)
    logger.info("TRAINING MODELS")
    logger.info("=" * 60)

    lr_model = trainer.train_logistic_regression(X_train, y_train)
    nb_model = trainer.train_naive_bayes(X_train, y_train)

    # Evaluate models
    logger.info("\n" + "=" * 60)
    logger.info("MODEL EVALUATION")
    logger.info("=" * 60)

    lr_results = trainer.evaluate_model(lr_model, X_test, y_test, "Logistic Regression")
    nb_results = trainer.evaluate_model(nb_model, X_test, y_test, "Naive Bayes")

    # Save models
    logger.info("\n" + "=" * 60)
    logger.info("SAVING MODELS")
    logger.info("=" * 60)

    trainer.save_models()

    # Summary
    logger.info("\n" + "=" * 60)
    logger.info("TRAINING SUMMARY")
    logger.info("=" * 60)
    logger.info(f"Logistic Regression Accuracy: {lr_results['accuracy']:.4f}")
    logger.info(f"Naive Bayes Accuracy: {nb_results['accuracy']:.4f}")
    logger.info(f"Models saved to: {model_dir}")


if __name__ == "__main__":
    train_sentiment_models()
