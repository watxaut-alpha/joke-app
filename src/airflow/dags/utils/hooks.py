from contextlib import closing

import pandas as pd
from airflow.hooks.postgres_hook import PostgresHook


class PostgresUpdateApiHook(PostgresHook):
    def __init__(self, *args, **kwargs):
        PostgresHook.__init__(self, *args, **kwargs)

    def update_column(self, table: str, column_name: str, df: pd.DataFrame, id_column_name="id", commit_every=1000):
        """
        A custom way to insert a set of tuples into a table,
        a new transaction is created every commit_every rows

        :param table: Name of the target table
        :param column_name: column name to update
        :param df: Dataframe with [id, column to update]
        :param id_column_name: name of the column to update
        :param commit_every: The maximum number of rows to insert in one
            transaction. Set to 0 to insert all rows in one transaction.
        """
        i = 0
        with closing(self.get_conn()) as conn:
            if self.supports_autocommit:
                self.set_autocommit(conn, False)

            conn.commit()

            with closing(conn.cursor()) as cur:
                for named_tuple in df.itertuples():
                    id_row = getattr(named_tuple, id_column_name)
                    value = getattr(named_tuple, column_name)
                    if type(value) is str:
                        value = f"'{value}'"
                    sql = f'update {table} set "{column_name}" = {value} where "{id_column_name}" = {id_row}'

                    cur.execute(sql)
                    i += 1
                    if commit_every and i % commit_every == 0:
                        conn.commit()
                        self.log.info("Loaded %s into %s rows so far", i, table)

            conn.commit()
        self.log.info("Done loading. Loaded a total of %s rows", i)
