from datetime import datetime, timedelta

# don't erase, Airflow will ignore the DAG if no airflow import is in the file
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

# set up DAG
dag_name = "test_db_postgres"
# schedule_interval = "0 0 * * *"
schedule_interval = "@once"
concurrency = 1
max_active_runs = 1

# DAG STRUCTURE
conn_id_source = "db"
conn_id_load = "db"

dag_args = {
    "retries": 2,
    "start_date": datetime(2020, 1, 10, 0, 0, 0),
    "owner": "airflow",
    "depends_on_past": False,
    "wait_for_downstream": False,
    "email": ["watxaut@gmail.com"],
    "email_on_failure": False,
    "email_on_retry": False,
    "retry_delay": timedelta(seconds=60),  # retry timing
    "dag_name": dag_name,
    "catchup": False,
    "max_active_runs": max_active_runs,
    "concurrency": concurrency,
}

dag = DAG(dag_name, default_args=dag_args, schedule_interval=schedule_interval)

sql = """
SELECT
   *
FROM
   pg_catalog.pg_tables
WHERE
   schemaname != 'pg_catalog' AND
   schemaname != 'information_schema';
"""
op_postgres = PostgresOperator(sql=sql, postgres_conn_id="db", task_id="test_db_postgres", dag=dag)
