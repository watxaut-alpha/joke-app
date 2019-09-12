import datetime
from sqlalchemy.engine import Engine

import src.db.core as db


def is_user_exists(conn: Engine, user_id: int) -> bool:
    df = db.execute_read(conn, "select id from users where user_id = {}".format(user_id))
    return df.empty


def add_user(conn: Engine, user_id: int, first_name: str) -> bool:

    if is_user_exists(conn, user_id):
        d_user = {
            "user_id": user_id,
            "name": first_name,
            "created_at": datetime.datetime.now().isoformat()
        }
        return db.add_record(conn, "users", d_user)
    else:
        # user already created
        return True
