import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine

from src.config import DB_HOST, POSTGRES_USER, POSTGRES_PASSWORD, SCHEMA_NAME


def connect(host: str, user: str, password: str, schema_name: str) -> Engine:
    engine = create_engine(
        "postgresql://{user}:{pwd}@{host}:5432/{schema_name}".format(
            user=user, pwd=password, host=host, schema_name=schema_name
        ),
        encoding="utf8",
    )

    return engine


def get_jokes_app_connection(host=None) -> Engine:
    if host is None:
        return connect(DB_HOST, POSTGRES_USER, POSTGRES_PASSWORD, SCHEMA_NAME)
    else:
        return connect(host, POSTGRES_USER, POSTGRES_PASSWORD, SCHEMA_NAME)


def execute_update(conn: Engine, postgres_query: str) -> bool:
    conn.execute(postgres_query)
    return True


def execute_read(conn: Engine, postgres_query: str) -> pd.DataFrame:
    return pd.read_sql(postgres_query, conn)


def add_record(conn: Engine, model: str, d_values: dict) -> bool:
    # workaround for inserting only one row with pandas DF
    d_values = {key: [value] for key, value in d_values.items()}

    # convert dict into Pandas DF
    df = pd.DataFrame(d_values)

    # store data in the Connection DB
    df.to_sql(model, con=conn, if_exists="append", index=False)
    return True


def add_records(conn: Engine, model: str, df: pd.DataFrame):
    df.to_sql(model, con=conn, if_exists="append", index=False)
    return True


def get_random_element(conn: Engine, table: str, where: str = "") -> pd.DataFrame:
    # query a random element
    if where == "":
        sql = "SELECT * FROM {table} ORDER BY random() LIMIT 1;".format(table=table)
    else:
        sql = "SELECT * FROM {table} where {where} ORDER BY random() LIMIT 1;".format(table=table, where=where)
    df = execute_read(conn, sql)
    return df
