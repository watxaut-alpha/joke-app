import src.db.core as db
import datetime


def get_random_joke(conn):
    # query new joke
    sql = "SELECT * FROM jokes ORDER BY random() LIMIT 1;"
    df = db.execute_query(conn, sql)
    return df


def insert_rating_joke(conn, user_id, joke_id, i_rating):

    model = "ratings"
    d_values = {
        "user_id": user_id,
        "joke_id": joke_id,
        "rating": i_rating,
        "created_at": datetime.datetime.now().isoformat()
    }
    db.add_record(conn, model, d_values)


def put_joke_db(conn, s_joke, s_author):
    model = "jokes"
    d_values = {
        "joke": s_joke,
        "author": s_author,
        "rating": 5,
        "tags": ""
    }

    db.add_record(conn, model, d_values)
