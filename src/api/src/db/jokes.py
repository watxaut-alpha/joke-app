import datetime
import sqlalchemy.exc
import pandas as pd
from sqlalchemy.engine import Engine

try:
    import src.db.core as db
except ModuleNotFoundError:
    import src.api.src.db.core as db


def get_random_joke() -> pd.DataFrame:
    conn = db.get_jokes_app_connection()
    return db.get_random_element(conn, "jokes")


def get_joke_not_sent_by_mail_already(conn: Engine, limit=1) -> pd.DataFrame:
    sql = """
    select
        *
    from
        jokes_to_send
    where
        jokes_to_send.id not in (select joke_id from sent_jokes) and
        (jokes_to_send.do_send is null or jokes_to_send.do_send != false)
    limit {limit}
    """.format(
        limit=limit
    )

    return db.execute_read(conn, sql)


def get_5_next_jokes_to_send():
    conn = db.get_jokes_app_connection()
    return get_joke_not_sent_by_mail_already(conn, limit=5)


def check_user_exists(user_id: str):
    sql_telegram = "select user_id from users where user_id='{user_id}'".format(user_id=user_id)
    sql_mail = "select id_hash from users_mail where id_hash='{user_id}'".format(user_id=user_id)

    conn = db.get_jokes_app_connection()

    has_telegram_user = not db.execute_read(conn, sql_telegram).empty
    has_mail_user = not db.execute_read(conn, sql_mail).empty

    if has_mail_user or has_telegram_user:
        return True  # at least one of the users exists
    else:
        return False  # the id does not correspond to telegram or mail users -> fake ID


def check_joke_id_exists(joke_id):
    sql = "select id from jokes where id={joke_id}".format(joke_id=joke_id)
    conn = db.get_jokes_app_connection()
    joke_id_exists = not db.execute_read(conn, sql).empty
    return joke_id_exists


def insert_rating_joke(user_id: str, joke_id: int, rating: float, source: str) -> bool:
    if check_user_exists(user_id) and check_joke_id_exists(joke_id):
        conn = db.get_jokes_app_connection()

        model = "ratings"
        d_values = {
            "user_id": user_id,
            "joke_id": joke_id,
            "rating": rating,
            "created_at": datetime.datetime.now().isoformat(),
            "source": source,
        }
        db.add_record(conn, model, d_values)
        return True
    else:
        return False


def upsert_rating_joke(user_id: str, joke_id: int, rating: float, source: str) -> bool:
    if check_user_exists(user_id) and check_joke_id_exists(joke_id):
        try:
            sql = """
        INSERT INTO ratings (user_id, joke_id, rating, created_at, source)
        VALUES ('{user_id}', {joke_id}, {rating}, '{created_at}', '{source}')
        ON CONFLICT (user_id, joke_id)
        DO UPDATE
        SET rating = {rating};
            """.format(
                user_id=user_id,
                joke_id=joke_id,
                rating=rating,
                created_at=datetime.datetime.now().isoformat(),
                source=source,
            )
            conn = db.get_jokes_app_connection()
            db.execute_update(conn, sql)
        except sqlalchemy.exc.ProgrammingError:
            return False

        return True
    else:
        return False  # id user does not exist in DB


def upsert_joke_tag(user_id: [str, int], joke_id: int, tag_id: int):
    sql = """
INSERT INTO joke_tags (user_id, joke_id, tag_id, created_at)
VALUES ('{user_id}', {joke_id}, {tag_id}, '{created_at}')
ON CONFLICT (user_id, joke_id, tag_id)
DO NOTHING;
        """.format(
        user_id=user_id, joke_id=joke_id, tag_id=tag_id, created_at=datetime.datetime.now().isoformat()
    )
    conn = db.get_jokes_app_connection()
    db.execute_update(conn, sql)


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
    return db.get_random_element(conn, "jokes", where="id not in (select joke_id from joke_tags group by joke_id)")
