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

## 6. Load / Prepare Data

**Code:** `src/data_pipeline/load.py`

**Input:** Cleaned DataFrame from `transform_data()`.

**Output path:** `data/processed/yellow_tripdata_2025-01_clean.parquet`

**Process:**
- Create `data/processed/` if it doesn't exist.
- Save cleaned data in Parquet format using Pandas.
- Preserve all cleaned records and engineered features.
- Make processed data reusable for model training.

**Status:** Successfully executed and verified.



## 7. Unit and Integration Testing — Completed

**Tool:** pytest 9.2.0

**Test directory:** `tests/`

### Test Coverage

| Test file | Purpose | Result |
|---|---|---|
| `test_transform.py` | Validate duration calculation, feature engineering, and invalid duration filtering | 2 Passed |
| `test_load.py` | Verify Parquet file creation and saved data integrity | 1 Passed |
| `test_extract.py` | Verify dataset download using a mocked HTTP response | 1 Passed |
| `test_airflow_dag.py` | Verify DAG imports, task definitions, and dependencies (`extract → transform_and_load`) | 1 Passed |
| `test_etl_integration.py` | Verify the complete Extract → Transform → Load process with sample data and temporary files | 1 Passed |

**Total:** 6 tests passed individually.

### Testing Techniques

- `assert`: Validate expected results.
- `tmp_path`: Create isolated temporary directories for test files.
- `monkeypatch`: Mock HTTP requests and redirect file operations without modifying project data.
- `DagBag`: Verify that Airflow can load the DAG and recognize its task dependencies.
- `BytesIO`: Create an in-memory Parquet file to simulate a dataset download.

### ETL Integration Test

The integration test verifies that the existing ETL functions work together correctly.

**Process:**

1. Create a sample dataset containing one valid and one invalid taxi trip.
2. Simulate the dataset download without accessing the internet.
3. Extract the raw Parquet file into a temporary directory.
4. Transform the data and filter out the invalid trip.
5. Save the cleaned dataset using the existing `load_data()` function.
6. Read the output and validate its contents.

**Validation:**
- The processed Parquet file exists.
- The invalid trip is removed.
- The valid trip has a duration of 15 minutes.
- `pickup_hour` and `pickup_day_of_week` are correctly generated.
- All four model features are present: `PULocationID`, `DOLocationID`, `pickup_hour`, and `pickup_day_of_week`.

The integration test uses temporary directories and does not modify the project's actual raw or processed datasets.

### Run Tests

**Full test suite:**

```bash
uv run python -m pytest tests/ -v
```

**ETL integration test:**

```bash
uv run python -m pytest tests/test_etl_integration.py -v
```

**Airflow DAG structure test:**

```bash
uv run python -m pytest tests/test_airflow_dag.py -v
```

### Status

**Completed:** All six tests passed individually, including the ETL integration test and the updated Airflow DAG structure test.

**Verified separately:** The Airflow DAG was executed successfully, producing the raw and processed Parquet files.

**Pending:** Execution of the complete pytest test suite in a single run.


## 8. Workflow Orchestration — Apache Airflow

**Tool:** Apache Airflow 3.4.0

**DAG file:** `dags/taxi_etl_dag.py`

**Pipeline:** `extract → transform_and_load`

**Purpose:**
- Automate ETL execution.
- Manage task dependencies.
- Monitor pipeline execution and failures.

**Implementation:**
- `@dag`: Define the workflow.
- `@task`: Define individual tasks.
- `>>`: Set task execution order.
- `dag_id="nyc_taxi_etl"`: Unique DAG identifier.
- `schedule=None`: Manual execution.
- `catchup=False`: Disable automatic catchup.
- `tags`: Organize DAGs in the Airflow UI.
- Import ETL functions directly from the installable `taxi_ml` Python package.

**Tasks:**
- `extract`: Download the January 2025 NYC Yellow Taxi dataset.
- `transform_and_load`: Clean the raw data, engineer features, and save the processed Parquet file.

**Design Decisions:**
- Reuse existing ETL functions without `subprocess.run()`.
- Combine Transform and Load to avoid transferring a large DataFrame through XCom.
- Avoid unnecessary intermediate staging files.

**Metadata Database:**
- SQLite is used for local development.
- Database location: `~/airflow/airflow.db`
- Database schema initialized using `airflow db migrate`.

**Testing:**
- DAG structure verified using `tests/test_airflow_dag.py`.
- Both tasks executed successfully through Airflow.
- Raw and processed Parquet files generated successfully.
- DAG run reached the `success` state.

**Execution Command:**

```bash
uv run airflow dags test nyc_taxi_etl -f dags/taxi_etl_dag.py
```

**Status:** DAG implementation, structural testing, and actual ETL execution completed successfully.










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
