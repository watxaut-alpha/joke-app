import pandas as pd
import datetime
from sqlalchemy.engine import Engine

from src.db.secret import SCHEMA_NAME, POSTGRES_USER, POSTGRES_PASSWORD
import src.db.core as db


def populate_jokes_db(host: str, path_json: str) -> None:

    engine = db.connect(host, POSTGRES_USER, POSTGRES_PASSWORD, SCHEMA_NAME)

    df_json = pd.read_json(path_json, encoding="utf8")
    df_json.to_sql('jokes', con=engine, if_exists='append', index=False)


# populate_jokes_db("vps721960.ovh.net", "/Users/joan/Documents/python_projects/joke_bot/newjokes2.json")


def add_telegram_log(conn: Engine, sender: str, message: str, id_user: int, item_1: str, var_txt_1: str) -> bool:
    d_telegram = {
        "sender": sender,
        "message": message,
        "user_id": id_user,
        "item_1": str(item_1),
        "var_txt_1": str(var_txt_1),
        "created_at": datetime.datetime.now().isoformat()
    }

    return db.add_record(conn, "telegram_log", d_telegram)


