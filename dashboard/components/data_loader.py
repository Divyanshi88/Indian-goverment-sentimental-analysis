"""Shared dashboard data loading."""

from __future__ import annotations

from pathlib import Path

import pandas as pd
import streamlit as st

from main import run_sample_pipeline
from src.utils.config import ROOT_DIR


@st.cache_data(show_spinner=False)
def load_content() -> pd.DataFrame:
    """Load processed content, generating sample data on first run."""
    processed_path = ROOT_DIR / "data" / "processed" / "sentiment_content.csv"
    if not processed_path.exists():
        run_sample_pipeline()
    frame = pd.read_csv(processed_path)
    frame["created_utc"] = pd.to_datetime(frame["created_utc"], errors="coerce", utc=True)
    frame["date"] = frame["created_utc"].dt.date
    return frame.dropna(subset=["created_utc"])


def asset_path(filename: str) -> Path:
    """Return an absolute path for a dashboard asset."""
    return ROOT_DIR / "dashboard" / "assets" / filename
