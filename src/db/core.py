from sqlalchemy import create_engine
import pandas as pd

from src.db.secret import host, POSTGRES_USER, POSTGRES_PASSWORD, s_db_name


def connect(s_host, user, password, db_name):
    engine = create_engine("postgresql://{user}:{pwd}@{host}:5432/{db_name}".format(
        user=user,
        pwd=password,
        host=s_host,
        db_name=db_name),
        encoding="utf8"
    )

    return engine


def get_jokes_app_connection():
    return connect(host, POSTGRES_USER, POSTGRES_PASSWORD, s_db_name)


def execute_update(conn, postgres_query):
    conn.execute(postgres_query)
    return True


def execute_read(connection, postgres_query):
    return pd.read_sql(postgres_query, connection)


def add_record(connection, model, d_values):
    # workaround for inserting only one row with pandas DF
    d_values = {key: [value] for key, value in d_values.items()}

    # convert dict into Pandas DF
    df = pd.DataFrame(d_values)

    # store data in the Connection DB
    df.to_sql(model, con=connection, if_exists='append', index=False)

    return True


def get_random_element(conn, table, where=""):

    # query a random element
    if where == "":
        sql = "SELECT * FROM {table} ORDER BY random() LIMIT 1;".format(table=table)
    else:
        sql = "SELECT * FROM {table} where {where} ORDER BY random() LIMIT 1;".format(table=table, where=where)
    df = execute_read(conn, sql)
    return df
