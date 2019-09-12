import datetime
from sqlalchemy.engine import Engine
import pandas as pd


import src.db.core as db


def has_twitter_db_joke(conn: Engine, tweet_str_id: str) -> bool:
    df = db.execute_read(conn, "select tweet_str_id from validate_twitter_jokes where tweet_str_id = '{}'".format(
        tweet_str_id))
    return not df.empty


def add_joke_to_twitter_table(conn: Engine, d_joke: dict) -> None:
    model = "validate_twitter_jokes"

    # d_joke already has the same parameters and column names as in the table
    d_joke["created_at"] = datetime.datetime.now().isoformat()

    db.add_record(conn, model, d_joke)


def get_random_twitter_joke(conn: Engine) -> pd.DataFrame:
    return db.get_random_element(conn, "validate_twitter_jokes", where="is_joke is null")


def update_joke_validation(conn: Engine, tweet_str_id: str, validated_by_user: int, is_joke: bool) -> None:
    sql = """
update 
    validate_twitter_jokes 
set 
    is_joke = {is_joke}, 
    validated_by_user_id = {validated_by_user}, 
    updated_at='{updated_at}'
where 
    id = {tweet_str_id}

""".format(
        is_joke=is_joke,
        validated_by_user=validated_by_user,
        updated_at=datetime.datetime.now().isoformat(),
        tweet_str_id=tweet_str_id
    )

    db.execute_update(conn, sql)

