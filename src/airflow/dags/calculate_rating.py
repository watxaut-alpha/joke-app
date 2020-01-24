from datetime import datetime, timedelta

# don't erase, Airflow will ignore the DAG if no airflow import is in the file
from airflow import DAG
from airflow.operators.postgres_operator import PostgresOperator

# set up DAG
dag_name = "dag_calculate_ratings"
schedule_interval = "0 20 * * *"
# schedule_interval = "@once"
concurrency = 1
max_active_runs = 1

# DAG STRUCTURE
conn_id_extract = "db"
conn_id_load = "db"

dag_args = {
    "retries": 2,
    "start_date": datetime(2020, 1, 23, 0, 0, 0),
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

sql = """
update
    jokes_to_send as jts
set
    rating = sr.mean
from
    (
        select
            r.joke_id, avg(r.rating) as mean
        from
            ratings r
        group by r.joke_id
    ) sr
where
    sr.joke_id = jts.id
"""

op_validate = PostgresOperator(sql=sql, task_id="calculate_ratings", postgres_conn_id=conn_id_extract, dag=dag)
