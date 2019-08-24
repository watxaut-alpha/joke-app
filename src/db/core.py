from sqlalchemy import create_engine
import pandas as pd


def connect(host, user, password, db_name):
    engine = create_engine("postgresql://{user}:{pwd}@{host}:5432/{db_name}".format(
            user=user,
            pwd=password,
            host=host,
            db_name=db_name),
        encoding="utf8"
    )

    return engine


def execute_query(connection, postgres_query):
    return pd.read_sql(postgres_query, connection)
