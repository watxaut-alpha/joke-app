import datetime
import uuid
from sqlalchemy.engine import Engine

try:
    import src.db.core as db
except ModuleNotFoundError:
    import src.api.src.db.core as db


def has_db_telegram_user(conn: Engine, user_id: str) -> bool:
    df = db.execute_read(conn, "select id from users where user_id = '{}'".format(user_id))
    return not df.empty  # returns true if the user is in the DB


def add_user_telegram(user_id: str, first_name: str) -> bool:

    conn = db.get_jokes_app_connection()

    if not has_db_telegram_user(conn, user_id):
        d_user = {"user_id": user_id, "name": first_name, "created_at": datetime.datetime.now().isoformat()}
        return db.add_record(conn, "users", d_user)
    else:
        # user already created
        return True


def get_users_mail():
    conn = db.get_jokes_app_connection()
    return db.execute_read(conn, "select * from users_mail")


def has_db_mail_user(conn: Engine, email: str) -> bool:
    df = db.execute_read(conn, "select email from users_mail where email='{}'".format(email))
    return not df.empty


def add_user_mail(email: str) -> bool:

    conn = db.get_jokes_app_connection()
    if not has_db_mail_user(conn, email):
        s_uuid = str(uuid.uuid1())
        d_user_mail = {"email": email, "id_hash": s_uuid, "created_at": datetime.datetime.now().isoformat()}

        db.add_record(conn, "users_mail", d_user_mail)
    else:
        print("User with email: '{}' already exists. Skipping..".format(email))
    return True


def add_admin_user(conn: Engine, username: str, email: str, hashed_password: str, disabled: bool, scopes: str) -> bool:
    # conn = db.get_jokes_app_connection()

    d_user_admin = {
        "username": username,
        "email": email,
        "hashed_password": hashed_password,
        "disabled": disabled,
        "scopes": scopes,
    }
    db.add_record(conn, "users_admin", d_user_admin)

    return True


def get_admin_users():
    conn = db.get_jokes_app_connection()
    return db.execute_read(conn, "select * from users_admin")


# from src.db.secret import HOST_OVH, POSTGRES_USER, POSTGRES_PASSWORD_OVH, SCHEMA_NAME
# conn = db.connect(HOST_OVH, POSTGRES_USER, POSTGRES_PASSWORD_OVH, SCHEMA_NAME)
#
# add_admin_user(conn, username, email, hashed_password, disabled, scopes)
