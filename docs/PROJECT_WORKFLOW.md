# MLE Model Deployment — Project Workflow

## 1. Project Overview

**Goal:** Predict NYC Yellow Taxi trip duration using Machine Learning.

- Dataset: January 2025 NYC Yellow Taxi
- Model: RandomForestRegressor
- Target: `duration` (minutes)
- Evaluation: RMSE
- Deployment: FastAPI (local)
- Experiment tracking: MLflow

## 2. Project Setup — Completed

- Git/GitHub: Version control
- Python 3.13: Programming language
- uv: Dependency and environment management
- `pyproject.toml`: Project dependencies
- `uv.lock`: Locked dependency versions

## 3. Extract Data — Completed

**Code:** `src/data_pipeline/extract.py`

**Source:** NYC Taxi & Limousine Commission (TLC)

**Dataset URL:**

https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet

**Raw data path:**

`data/raw/yellow_tripdata_2025-01.parquet`

**Process:**
- Download January 2025 Yellow Taxi data using `requests`.
- Create the raw directory automatically.
- Skip download if the file already exists.
- Preserve original data.

## 4. Exploratory Data Analysis — Completed

**Notebook:** `notebooks/01_data_exploration.ipynb`

**Dataset:** 3,475,226 rows × 20 columns.

### Dataset Features

| Feature | Description |
|---|---|
| `VendorID` | Taxi provider |
| `tpep_pickup_datetime` | Pickup timestamp |
| `tpep_dropoff_datetime` | Dropoff timestamp |
| `passenger_count` | Passenger count |
| `trip_distance` | Distance in miles |
| `RatecodeID` | Fare category |
| `store_and_fwd_flag` | Data storage flag |
| `PULocationID` | Pickup zone |
| `DOLocationID` | Dropoff zone |
| `payment_type` | Payment method |
| `fare_amount` | Fare |
| `extra` | Extra charges |
| `mta_tax` | MTA tax |
| `tip_amount` | Tip |
| `tolls_amount` | Tolls |
| `improvement_surcharge` | Improvement fee |
| `total_amount` | Total charge |
| `congestion_surcharge` | Congestion fee |
| `Airport_fee` | Airport fee |
| `cbd_congestion_fee` | CBD congestion fee |

### Target Variable

`duration = (dropoff_datetime - pickup_datetime) / 60 seconds`

**Unit:** Minutes.

### Important Findings

- Negative durations: 124
- Zero durations: 1,927
- Zero-distance trips: 90,893
- Trips over 60 minutes: 31,867
- Distances over 1,000 miles: 116
- Trips with average speed over 65 mph: 1,090
- Pickup/dropoff location IDs: No missing, zero, or negative IDs found

## 5. Transform Data — In Progress

**Code:** `src/data_pipeline/transform.py`

**Purpose:** Clean invalid records and prepare model features.

### Cleaning Rules

| Rule | Reason |
|---|---|
| Pickup in January 2025 | Match dataset period |
| Duration: 1–180 minutes | Exclude invalid/extreme durations |
| Distance > 0 miles | Exclude zero-distance trips |
| Average speed ≤ 65 mph | Remove implausible trips |

These are initial assumptions, subject to evaluation.

### Feature Engineering

- `duration`: Prediction target, in minutes
- `pickup_hour`: Pickup hour (0–23)
- `pickup_day_of_week`: Day of week (0–6)

### Candidate Model Features

- `PULocationID`
- `DOLocationID`
- `pickup_hour`
- `pickup_day_of_week`

**Note:** Recorded final trip distance and dropoff time are unavailable at pickup, so they should not be used as inputs for a pickup-time prediction model.

## 6. Load / Prepare Data — Completed

**Code:** `src/data_pipeline/load.py`

**Input:** Cleaned DataFrame from `transform_data()`.

**Output path:** `data/processed/yellow_tripdata_2025-01_clean.parquet`

**Process:**
- Create `data/processed/` if it doesn't exist.
- Save cleaned data in Parquet format using Pandas.
- Preserve all cleaned records and engineered features.
- Make processed data reusable for model training.

**Status:** Successfully executed and verified.







## 7. Model Training — Planned

- Train `RandomForestRegressor`.
- Evaluate using RMSE.
- Track experiments with MLflow.
- Optional: GridSearchCV / Optuna.

## 8. Model Deployment — Planned

- FastAPI: Prediction service
- `/predict`: Prediction endpoint
- Uvicorn: Local server
- cURL / Requests: API validation
- Docker: Optional

## 9. Final Results — Pending

**Final RMSE:** To be measured.

**What would I do differently with more time?** To be answered after model evaluation.
