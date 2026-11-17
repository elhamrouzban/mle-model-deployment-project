
import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Calculate trip duration in minutes
    df["duration"] = (
        df["tpep_dropoff_datetime"]
        - df["tpep_pickup_datetime"]
    ).dt.total_seconds() / 60

    # Keep trips starting in January 2025
    df = df[
        (df["tpep_pickup_datetime"] >= "2025-01-01")
        & (df["tpep_pickup_datetime"] < "2025-02-01")
    ].copy()

    # Remove invalid durations and distances
    df = df[df["duration"].between(1, 180)].copy()
    df = df[df["trip_distance"] > 0].copy()

    # Remove unrealistic average speeds
    speed_mph = df["trip_distance"] / (df["duration"] / 60)
    df = df[speed_mph <= 65].copy()

    # Create features for model training
    df["pickup_hour"] = df["tpep_pickup_datetime"].dt.hour
    df["pickup_day_of_week"] = df["tpep_pickup_datetime"].dt.dayofweek

    return df.reset_index(drop=True)
