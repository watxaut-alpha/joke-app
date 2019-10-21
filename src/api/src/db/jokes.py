import datetime

import pandas as pd
from sqlalchemy.engine import Engine

try:
    import src.db.core as db
except ModuleNotFoundError:
    import src.api.src.db.core as db


def get_random_joke() -> pd.DataFrame:
    conn = db.get_jokes_app_connection()
    return db.get_random_element(conn, "jokes")


def get_random_joke_not_sent_by_mail_already(conn: Engine) -> pd.DataFrame:
    return db.get_random_element(
        conn, "jokes", "jokes.id not in (select joke_id from sent_jokes)"
    )


def insert_rating_joke(user_id: [str, int], joke_id: int, rating: float) -> None:
    conn = db.get_jokes_app_connection()

    model = "ratings"
    d_values = {
        "user_id": user_id,
        "joke_id": joke_id,
        "rating": rating,
        "created_at": datetime.datetime.now().isoformat(),
    }
    db.add_record(conn, model, d_values)


def upsert_rating_joke(user_id: [str, int], joke_id: int, rating: float) -> None:
    sql = """
INSERT INTO ratings (user_id, joke_id, rating, created_at) 
VALUES ('{user_id}', {joke_id}, {rating}, '{created_at}')
ON CONFLICT (user_id, joke_id) 
DO UPDATE 
SET rating = {rating};
    """.format(
        user_id=user_id,
        joke_id=joke_id,
        rating=rating,
        created_at=datetime.datetime.now().isoformat(),
    )
    conn = db.get_jokes_app_connection()
    db.execute_update(conn, sql)


def upsert_joke_tag(user_id: [str, int], joke_id: int, tag_id: int):
    sql = """
INSERT INTO joke_tags (user_id, joke_id, tag_id, created_at) 
VALUES ('{user_id}', {joke_id}, {tag_id}, '{created_at}')
ON CONFLICT (user_id, joke_id, tag_id) 
DO NOTHING;
        """.format(
        user_id=user_id,
        joke_id=joke_id,
        tag_id=tag_id,
        created_at=datetime.datetime.now().isoformat(),
    )
    conn = db.get_jokes_app_connection()
    a = db.execute_update(conn, sql)
    print(a, 2)


def put_joke_db(conn: Engine, joke: str, author: str) -> None:
    model = "jokes"
    d_values = {
        "joke": joke,
        "author": author,
        "rating": 5,
        "tags": "",
        "created_at": datetime.datetime.now().isoformat(),
    }
    db.add_record(conn, model, d_values)


def put_sent_joke_db(conn: Engine, joke_id: int) -> None:
    model = "sent_jokes"
    d_values = {"joke_id": joke_id, "created_at": datetime.datetime.now().isoformat()}
    db.add_record(conn, model, d_values)


def get_tags():
    conn = db.get_jokes_app_connection()
    sql = "select * from tags"
    df_tags = db.execute_read(conn, sql)
    return df_tags.to_dict(orient="index")


def get_untagged_joke():
    conn = db.get_jokes_app_connection()
    return db.get_random_element(
        conn,
        "jokes",
        where="id not in (select joke_id from joke_tags group by joke_id)",
    )
