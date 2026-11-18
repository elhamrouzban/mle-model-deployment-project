from pathlib import Path
import pandas as pd

PROCESSED_DIR = Path("data/processed")


def load_data(df: pd.DataFrame) -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    output_path = PROCESSED_DIR / "yellow_tripdata_2025-01_clean.parquet"
    df.to_parquet(output_path, index=False)

    print(f"Processed data saved to: {output_path}")
