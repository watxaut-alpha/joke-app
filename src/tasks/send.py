import logging

import src.tasks.mail.core as mail
import src.tasks.mail.smtp as smtp
import src.api.src.db.jokes as jokes
import src.api.src.db.core as db
import src.api.src.db.users as users
from src.tasks.mail.secret import YAHOO_USER as USER, YAHOO_PWD as PASSWORD


def send_mail():
    logger = logging.getLogger("jokeBot")

    conn = db.get_jokes_app_connection()

    d_receivers = users.get_users_mail(conn).to_dict(orient="index")

    # get a joke that is not sent previously
    df_joke = jokes.get_random_joke_not_sent_by_mail_already(conn)
    if df_joke.empty:  # no more jokes in the DB???
        return smtp.send_mail_watxaut(USER, PASSWORD, "NO MORE JOKES IN DB!!!")

    # else, there is still jokes so unpack
    d_joke = df_joke.to_dict(orient="index")[0]
    d_joke["joke"] = d_joke["joke"].replace("\n", "<br>")  # replace \n with html

    is_sent = mail.send_mail(USER, PASSWORD, d_receivers, d_joke, mail.SUBJECT, provider="smtp")

    if is_sent:
        jokes.put_sent_joke_db(conn, d_joke["id"])
        logger.info("Joke sent via mail with joke_id='{}'".format(d_joke["id"]))
    else:
        logger.error("Joke not sent! joke_id='{}'".format(d_joke["id"]))

    return is_sent
