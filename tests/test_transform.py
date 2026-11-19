
import pandas as pd

from taxi_ml.data_pipeline.transform import transform_data


def test_feature_engineering():
    # Arrange: Create a sample trip
    df = pd.DataFrame({
        "tpep_pickup_datetime": [
            pd.Timestamp("2025-01-15 10:00:00")
        ],
        "tpep_dropoff_datetime": [
            pd.Timestamp("2025-01-15 10:25:00")
        ],
        "trip_distance": [5.0],
    })

    # Act: Transform the data
    result = transform_data(df)

    # Assert: Verify the results
    assert len(result) == 1
    assert result["duration"].iloc[0] == 25
    assert result["pickup_hour"].iloc[0] == 10
    assert result["pickup_day_of_week"].iloc[0] == 2



def test_invalid_duration():
    df = pd.DataFrame({
        "tpep_pickup_datetime": [
            pd.Timestamp("2025-01-15 10:00:00"),
            pd.Timestamp("2025-01-15 10:00:00"),
        ],
        "tpep_dropoff_datetime": [
            pd.Timestamp("2025-01-15 09:50:00"),  # -10 minutes
            pd.Timestamp("2025-01-15 10:20:00"),  # 20 minutes
        ],
        "trip_distance": [2.0, 3.0],
    })

    result = transform_data(df)

    assert len(result) == 1
    assert result["duration"].iloc[0] == 20