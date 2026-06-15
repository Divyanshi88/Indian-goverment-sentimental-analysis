"""Configuration loading utilities."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - optional local convenience dependency
    load_dotenv = None

ROOT_DIR = Path(__file__).resolve().parents[2]
CONFIG_PATH = ROOT_DIR / "config" / "settings.yaml"


def load_config(path: Path | None = None) -> dict[str, Any]:
    """Load YAML configuration and environment variables."""
    if load_dotenv is not None:
        load_dotenv(ROOT_DIR / ".env")
    config_file = path or CONFIG_PATH
    with config_file.open("r", encoding="utf-8") as file:
        return yaml.safe_load(file)
