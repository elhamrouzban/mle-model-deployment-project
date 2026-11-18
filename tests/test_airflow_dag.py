from airflow.dag_processing.dagbag import DagBag


def test_taxi_etl_dag():
    dagbag = DagBag(dag_folder="dags")

    assert not dagbag.import_errors

    dag = dagbag.dags.get("nyc_taxi_etl")
    assert dag is not None

    assert set(dag.task_ids) == {
        "extract",
        "transform_and_load",
    }

    assert dag.get_task("extract").downstream_task_ids == {
        "transform_and_load"
    }