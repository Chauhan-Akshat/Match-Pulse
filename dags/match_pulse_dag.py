from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys

sys.path.insert(0, "/opt/airflow/src")

from extract import fetch_completed_matches
from transform import transform_matches, generate_date_dim
from load import load_all

default_args = {
    "owner": "akshat",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

def run_etl():
    raw = fetch_completed_matches(season=2024)
    transformed = transform_matches(raw)
    date_df = generate_date_dim(transformed["matches"])
    load_all(transformed, date_df)

with DAG(
    dag_id="match_pulse_etl",
    default_args=default_args,
    description="Daily ETL pulling completed football matches into the warehouse",
    schedule="@daily",
    start_date=datetime(2026, 8, 1),
    catchup=False,
    tags=["match-pulse"],
) as dag:

    etl_task = PythonOperator(
        task_id="extract_transform_load",
        python_callable=run_etl,
    )