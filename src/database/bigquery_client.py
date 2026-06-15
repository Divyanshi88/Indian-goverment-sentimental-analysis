"""Google BigQuery storage adapter."""

from __future__ import annotations

import os

import pandas as pd

try:
    from google.cloud import bigquery
except ImportError:  # pragma: no cover - optional cloud dependency
    bigquery = None


def get_bigquery_client() -> bigquery.Client:
    """Create a BigQuery client from environment configuration."""
    if bigquery is None:
        raise RuntimeError("google-cloud-bigquery is not installed.")
    project = os.getenv("GCP_PROJECT_ID")
    if not project:
        raise RuntimeError("GCP_PROJECT_ID is required for BigQuery operations.")
    return bigquery.Client(project=project)


def upload_dataframe(
    frame: pd.DataFrame,
    table_name: str,
    dataset: str,
    if_exists: str = "WRITE_APPEND",
) -> bigquery.job.LoadJob:
    """Upload a dataframe to BigQuery."""
    client = get_bigquery_client()
    table_id = f"{client.project}.{dataset}.{table_name}"
    job_config = bigquery.LoadJobConfig(write_disposition=if_exists, autodetect=True)
    job = client.load_table_from_dataframe(frame, table_id, job_config=job_config)
    job.result()
    return job
