import src.db.core as db


def get_random_joke(conn):
    # query new joke
    sql = "SELECT * FROM jokes ORDER BY random() LIMIT 1;"
    df = db.execute_query(conn, sql)
    return df
