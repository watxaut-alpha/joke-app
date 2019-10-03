import datetime
from sqlalchemy.engine import Engine
import pandas as pd

import src.db.core as db


def get_random_joke(conn: Engine) -> pd.DataFrame:
    return db.get_random_element(conn, "jokes")


def get_random_joke_not_sent_by_mail_already(conn: Engine) -> pd.DataFrame:
    return db.get_random_element(conn, "jokes", "jokes.id not in (select joke_id from sent_jokes)")


def insert_rating_joke(conn: Engine, user_id: int, joke_id: int, rating: float) -> None:

    model = "ratings"
    d_values = {
        "user_id": user_id,
        "joke_id": joke_id,
        "rating": rating,
        "created_at": datetime.datetime.now().isoformat()
    }
    db.add_record(conn, model, d_values)


def put_joke_db(conn: Engine, joke: str, author: str) -> None:
    model = "jokes"
    d_values = {
        "joke": joke,
        "author": author,
        "rating": 5,
        "tags": ""
    }

    db.add_record(conn, model, d_values)


def put_sent_joke_db(conn: Engine, joke_id: int) -> None:
    model = "sent_jokes"
    d_values = {
        "joke_id": joke_id,
        "created_at": datetime.datetime.now().isoformat()
    }

    db.add_record(conn, model, d_values)
