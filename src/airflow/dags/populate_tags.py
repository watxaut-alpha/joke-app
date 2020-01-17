from datetime import datetime, timedelta

# don't erase, Airflow will ignore the DAG if no airflow import is in the file
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

import utils.helpers as helpers

# set up DAG
dag_name = "dag_populate_tags"
schedule_interval = "0 1 * * *"
# schedule_interval = "@once"
concurrency = 1
max_active_runs = 1

# DAG STRUCTURE
conn_id_extract = "db"
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
    "retry_delay": timedelta(seconds=20),  # retry timing
    "dag_name": dag_name,
    "catchup": False,
    "max_active_runs": max_active_runs,
    "concurrency": concurrency,
}

dag = DAG(dag_name, default_args=dag_args, schedule_interval=schedule_interval)

op_validate = PythonOperator(
    task_id="insert_tags_jokes",
    op_kwargs={"conn_id_extract": conn_id_extract, "conn_id_load": conn_id_load},
    python_callable=helpers.put_tags_jokes,
    dag=dag,
)
