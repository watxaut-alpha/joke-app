from src.db.secret import host, db_name, POSTGRES_USER, POSTGRES_PASSWORD
import src.db.core as db
import pandas as pd


def populate_jokes_db(path_json):

    engine = db.connect(host, POSTGRES_USER, POSTGRES_PASSWORD, db_name)

    df_json = pd.read_json(path_json, encoding="utf8")
    df_json.to_sql('jokes', con=engine, if_exists='replace', index_label='id')

