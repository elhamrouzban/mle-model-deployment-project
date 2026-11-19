
from io import BytesIO

import pandas as pd

from taxi_ml.data_pipeline import extract, load
from taxi_ml.data_pipeline.transform import transform_data


def create_sample_data():
    return pd.DataFrame({
        "tpep_pickup_datetime": pd.to_datetime([
            "2025-01-15 10:00:00",
            "2025-01-15 11:00:00",
        ]),
        "tpep_dropoff_datetime": pd.to_datetime([
            "2025-01-15 10:15:00",
            "2025-01-15 11:00:00",
        ]),
        "PULocationID": [161, 237],
        "DOLocationID": [236, 161],
        "trip_distance": [3.0, 2.0],
    })


def test_etl_pipeline(tmp_path, monkeypatch):
    # Prepare test data as Parquet bytes
    sample = create_sample_data()

    buffer = BytesIO()
    sample.to_parquet(buffer, index=False)

    # Mock the HTTP response
    class FakeResponse:
        content = buffer.getvalue()

        def raise_for_status(self):
            pass

    monkeypatch.setattr(
        extract.requests,
        "get",
        lambda *args, **kwargs: FakeResponse(),
    )

    # Redirect files to temporary directories
    monkeypatch.setattr(extract, "RAW_DIR", tmp_path / "raw")
    monkeypatch.setattr(load, "PROCESSED_DIR", tmp_path / "processed")

    # Extract
    extract.download_data()

    raw_file = extract.RAW_DIR / "yellow_tripdata_2025-01.parquet"
    assert raw_file.exists()

    # Transform
    df = pd.read_parquet(raw_file)
    df_clean = transform_data(df)

    # Load
    load.load_data(df_clean)

    output_file = (
        load.PROCESSED_DIR / "yellow_tripdata_2025-01_clean.parquet"
    )

    # Validate the final output
    assert output_file.exists()

    result = pd.read_parquet(output_file)

    assert len(result) == 1
    assert result["duration"].iloc[0] == 15
    assert result["pickup_hour"].iloc[0] == 10
    assert result["pickup_day_of_week"].iloc[0] == 2

    expected_features = {
        "PULocationID",
        "DOLocationID",
        "pickup_hour",
        "pickup_day_of_week",
    }

    assert expected_features.issubset(result.columns)
    assert result["PULocationID"].iloc[0] == 161
    assert result["DOLocationID"].iloc[0] == 236
