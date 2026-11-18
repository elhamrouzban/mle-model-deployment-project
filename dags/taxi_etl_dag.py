
from datetime import datetime
from pathlib import Path
from subprocess import run

from airflow.sdk import dag, task

# Absolute path to the project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]


def run_project_code(code: str):
    run(
        ["uv", "run", "python", "-c", code],
        cwd=PROJECT_ROOT,
        check=True,
    )


@dag(
    dag_id="nyc_taxi_etl",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    tags=["nyc-taxi", "etl"],
)
def taxi_etl_pipeline():

    @task
    def extract():
        run_project_code(
            "from src.data_pipeline.extract import download_data; "
            "download_data()"
        )

    @task
    def transform():
        run_project_code(
            "import pandas as pd; "
            "from src.data_pipeline.transform import transform_data; "
            "df = pd.read_parquet('data/raw/yellow_tripdata_2025-01.parquet'); "
            "clean = transform_data(df); "
            "clean.to_parquet('data/processed/yellow_tripdata_2025-01_clean.parquet', index=False)"
        )

    @task
    def load():
        run_project_code(
            "import pandas as pd; "
            "from src.data_pipeline.load import load_data; "
            "df = pd.read_parquet('data/processed/yellow_tripdata_2025-01_clean.parquet'); "
            "load_data(df)"
        )

    extract() >> transform() >> load()


taxi_etl_pipeline()
