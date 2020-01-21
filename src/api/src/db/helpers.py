import pandas as pd

from src.config import SCHEMA_NAME, POSTGRES_USER, POSTGRES_PASSWORD
import src.db.core as db


def populate_jokes_db(host: str, path_json: str) -> None:

    engine = db.connect(host, POSTGRES_USER, POSTGRES_PASSWORD, SCHEMA_NAME)

    df_json = pd.read_json(path_json, encoding="utf8")
    df_json.to_sql("jokes_to_send", con=engine, if_exists="append", index=False)
