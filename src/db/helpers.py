from src.db.secret import host, s_db_name, POSTGRES_USER, POSTGRES_PASSWORD
import src.db.core as db
import pandas as pd
import datetime


def populate_jokes_db(s_host, path_json):

    engine = db.connect(s_host, POSTGRES_USER, POSTGRES_PASSWORD, s_db_name)

    df_json = pd.read_json(path_json, encoding="utf8")
    df_json.to_sql('jokes', con=engine, if_exists='append', index=False)


# populate_jokes_db("vps721960.ovh.net", "/Users/joan/Documents/python_projects/joke_bot/newjokes2.json")


def add_telegram_log(conn, sender, message, id_user, item_1, var_txt_1):
    d_telegram = {
        "sender": sender,
        "message": message,
        "user_id": id_user,
        "item_1": str(item_1),
        "var_txt_1": str(var_txt_1),
        "created_at": datetime.datetime.now().isoformat()
    }

    return db.add_record(conn, "telegram_log", d_telegram)


