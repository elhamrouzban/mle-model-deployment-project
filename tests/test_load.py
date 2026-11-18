
import pandas as pd

from src.data_pipeline import load


def test_load_data(tmp_path, monkeypatch):
    # Arrange: Create sample data
    df = pd.DataFrame({
        "duration": [15.0, 25.0],
        "PULocationID": [100, 200],
    })

    # Use a temporary directory
    monkeypatch.setattr(load, "PROCESSED_DIR", tmp_path)

    # Act: Save the data
    load.load_data(df)

    # Assert: Check that the file exists
    output = tmp_path / "yellow_tripdata_2025-01_clean.parquet"
    assert output.exists()

    # Verify saved content
    saved_df = pd.read_parquet(output)
    pd.testing.assert_frame_equal(saved_df, df)
