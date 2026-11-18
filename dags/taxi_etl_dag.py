
from pathlib import Path

import pandas as pd
from airflow.sdk import dag, task

from src.data_pipeline.extract import download_data
from src.data_pipeline.transform import transform_data
from src.data_pipeline.load import load_data


RAW_PATH = Path("data/raw/yellow_tripdata_2025-01.parquet")


@dag(
    dag_id="nyc_taxi_etl",
    schedule=None,
    catchup=False,
    tags=["nyc-taxi", "etl"],
)
def taxi_etl_pipeline():

    @task
    def extract():
        download_data()

    @task
    def transform_and_load():
        df = pd.read_parquet(RAW_PATH)

        df_clean = transform_data(df)

        load_data(df_clean)

    extract() >> transform_and_load()


taxi_etl_pipeline()
