import logging

import src.api.src.mail.core as mail
import src.api.src.mail.smtp as smtp
import src.api.src.db.jokes as jokes
import src.api.src.db.core as db
import src.api.src.db.users as users
from src.api.src.mail.secret import MAILGUN_USER as USER, MAILGUN_PWD as PASSWORD


def send_mail():
    logger = logging.getLogger("jokeBot")

    conn = db.get_jokes_app_connection()

    d_receivers = users.get_users_mail().to_dict(orient="index")

    # get a joke that is not sent previously
    df_joke = jokes.get_joke_not_sent_by_mail_already(conn)
    if df_joke.empty:  # no more jokes in the DB???
        return smtp.send_mail_watxaut(USER, PASSWORD, "NO MORE JOKES IN DB!!!")

    # else, there is still jokes so unpack
    d_joke = df_joke.to_dict(orient="index")[0]

    # add author if any
    if d_joke["author"] not in [None, ""]:
        d_joke["joke"] += "\n\nby {}".format(d_joke["author"])

    d_joke["joke"] = d_joke["joke"].replace("\n", "<br>")  # replace \n with html

    is_sent = mail.send_joke_mails(USER, PASSWORD, d_receivers, d_joke, provider="smtp")

    if is_sent:
        jokes.put_sent_joke_db(conn, d_joke["id"])
        logger.info("Joke sent via mail with joke_id='{}'".format(d_joke["id"]))
    else:
        logger.error("Joke not sent! joke_id='{}'".format(d_joke["id"]))

    return is_sent
