
from taxi_ml.data_pipeline import extract


def test_download_data(tmp_path, monkeypatch):
    # Use a temporary directory
    monkeypatch.setattr(extract, "RAW_DIR", tmp_path)

    # Simulate a successful HTTP response
    class FakeResponse:
        content = b"fake parquet content"

        def raise_for_status(self):
            pass

    def fake_get(url, timeout):
        assert url.endswith("yellow_tripdata_2025-01.parquet")
        return FakeResponse()

    monkeypatch.setattr(extract.requests, "get", fake_get)

    # Run extraction
    extract.download_data()

    # Check downloaded file
    output = tmp_path / "yellow_tripdata_2025-01.parquet"

    assert output.exists()
    assert output.read_bytes() == b"fake parquet content"
