import requests

import src.db.users as db_users
import src.mail.core as mail
from src.config import MAILGUN_USER, MAILGUN_PWD


def get_cat_url():
    r_cat = requests.get("https://api.thecatapi.com/v1/images/search")
    if r_cat:  # status 200
        url = r_cat.json()[0]["url"]
    else:
        url = "Cat not found"
    return url


def check_email(email: str):
    l_email = email.split("@")
    if len(l_email) != 2:
        return False
    if l_email[1].count(".") != 1:
        return False
    if l_email[0] == "":
        return False
    return True


async def put_user_db(email):
    if not check_email(email):
        return False

    db_users.add_user_mail(email)

    # send mail to subbed user
    is_sent = mail.send_subscribed_mail(MAILGUN_USER, MAILGUN_PWD, email)
    return is_sent
