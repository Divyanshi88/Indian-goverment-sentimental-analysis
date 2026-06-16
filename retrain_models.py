"""Retrain sentiment classification models with expanded dataset."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.models.sentiment import add_sentiment_labels
from src.models.train_models import SentimentModelTrainer
from src.preprocessing.text_cleaner import preprocess_posts, preprocess_comments
from src.utils.config import ROOT_DIR
from src.utils.logging import get_logger

logger = get_logger(__name__)


def retrain_with_newsapi_data() -> None:
    """Retrain models using combined original + NewsAPI data."""
    logger.info("=" * 70)
    logger.info("MODEL RETRAINING WITH EXPANDED DATASET")
    logger.info("=" * 70)

    # Load combined training data (already merged and labeled)
    combined_path = ROOT_DIR / "data" / "processed" / "combined_training.csv"
    
    if not combined_path.exists():
        logger.error(f"Combined training data not found at {combined_path}")
        logger.error("Run: python collect_training_data.py --mode combine")
        return

    logger.info(f"\nLoading combined training data...")
    training_data = pd.read_csv(combined_path)
    
    logger.info(f"Loaded {len(training_data)} total samples")
    logger.info(f"Sentiment distribution:\n{training_data['sentiment'].value_counts()}")

    # Check if we have enough data
    if len(training_data) < 3:
        logger.error("Not enough training data (minimum 3 samples required)")
        logger.error(f"Current samples: {len(training_data)}")
        return

    # Initialize trainer
    model_dir = ROOT_DIR / "src" / "models" / "trained_models"
    trainer = SentimentModelTrainer(model_dir=model_dir)

    # Prepare training data
    logger.info("\n" + "=" * 70)
    logger.info("PREPARING DATA")
    logger.info("=" * 70)

    X_train, X_test, y_train, y_test = trainer.prepare_data(
        training_data,
        text_column="clean_text",
        label_column="sentiment",
        test_size=0.2,
    )

    # Train models
    logger.info("\n" + "=" * 70)
    logger.info("TRAINING MODELS")
    logger.info("=" * 70)

    lr_model = trainer.train_logistic_regression(X_train, y_train)
    nb_model = trainer.train_naive_bayes(X_train, y_train)

    # Evaluate models
    logger.info("\n" + "=" * 70)
    logger.info("MODEL EVALUATION")
    logger.info("=" * 70)

    lr_results = trainer.evaluate_model(lr_model, X_test, y_test, "Logistic Regression")
    nb_results = trainer.evaluate_model(nb_model, X_test, y_test, "Naive Bayes")

    # Save models
    logger.info("\n" + "=" * 70)
    logger.info("SAVING MODELS")
    logger.info("=" * 70)

    trainer.save_models()

    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("RETRAINING SUMMARY")
    logger.info("=" * 70)
    logger.info(f"Total training samples: {len(training_data)}")
    logger.info(f"Train set: {X_train.shape[0]}, Test set: {X_test.shape[0]}")
    logger.info(f"\nLogistic Regression Accuracy: {lr_results['accuracy']:.4f}")
    logger.info(f"Naive Bayes Accuracy: {nb_results['accuracy']:.4f}")
    logger.info(f"\nModels saved to: {model_dir}")

    # Save training history
    history_path = model_dir / "training_history.txt"
    with open(history_path, "w") as f:
        f.write("Model Retraining History\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Training samples: {len(training_data)}\n")
        f.write(f"Train/Test split: {X_train.shape[0]}/{X_test.shape[0]}\n")
        f.write(f"\nLogistic Regression Accuracy: {lr_results['accuracy']:.4f}\n")
        f.write(f"Naive Bayes Accuracy: {nb_results['accuracy']:.4f}\n")
        f.write(f"\nClassification Report (Logistic Regression):\n")
        f.write(lr_results['classification_report'])
        f.write(f"\nClassification Report (Naive Bayes):\n")
        f.write(nb_results['classification_report'])

    logger.info(f"\nTraining history saved to: {history_path}")


if __name__ == "__main__":
    retrain_with_newsapi_data()
