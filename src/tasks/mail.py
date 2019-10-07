import logging

import src.mail.core as mail
import src.db.jokes as jokes
import src.db.core as db
from src.mail.secret import YAHOO_USER as USER, YAHOO_PWD as PASSWORD


def send_mail():
    logger = logging.getLogger("jokeBot")

    conn = db.get_jokes_app_connection()

    # get a joke that is not sent previously
    df_joke = jokes.get_random_joke_not_sent_by_mail_already(conn)
    s_joke = df_joke["joke"][0].replace("\n", "<br>")  # replace \n with html
    joke_id = int(df_joke["id"][0])

    is_sent = mail.send_mail(USER, PASSWORD, mail.RECEIVERS, s_joke, mail.SUBJECT, provider='smtp')

    if is_sent:
        jokes.put_sent_joke_db(conn, joke_id)
        logger.info("Joke sent via mail with joke_id='{}'".format(joke_id))
    else:
        logger.error("Joke not sent! joke_id='{}'".format(joke_id))

    return is_sent
