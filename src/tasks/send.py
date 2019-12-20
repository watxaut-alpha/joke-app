import logging

import src.api.src.db.core as db
import src.api.src.db.jokes as jokes
import src.api.src.db.users as users
import src.api.src.mail.core as mail
import src.api.src.mail.smtp as smtp
import src.web.twitter.twitter as twitter
from src.api.src.mail.secret import MAILGUN_USER as USER, MAILGUN_PWD as PASSWORD


def send_mail(is_debug):
    logger = logging.getLogger("jokeBot")

    host = "localhost"
    conn = db.get_jokes_app_connection(host)

    d_receivers = users.get_users_mail(is_debug, host=host).to_dict(orient="index")

    # get a joke that is not sent previously
    df_joke = jokes.get_joke_not_sent_by_pfm_already(conn, limit=1, sent_from="mail")
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
        if not is_debug:
            jokes.put_sent_joke_db(conn, d_joke["id"], sent_from="mail")
        logger.info("Joke sent via mail with joke_id='{}'".format(d_joke["id"]))
    else:
        logger.error("Joke not sent! joke_id='{}'".format(d_joke["id"]))

    return is_sent


def send_tweet():
    logger = logging.getLogger("jokeBot")

    host = "localhost"
    conn = db.get_jokes_app_connection(host)
    # get a joke that is not sent previously
    df_joke = jokes.get_joke_not_sent_by_pfm_already(conn, limit=1, sent_from="twitter")

    if df_joke.empty:  # no more jokes in the DB???
        return smtp.send_mail_watxaut(USER, PASSWORD, "NO MORE JOKES IN DB!!!")

    # else, there is still jokes so unpack
    d_joke = df_joke.to_dict(orient="index")[0]
    api = twitter.init_twitter_handler()
    response = twitter.send_tweet(api, d_joke["joke"])
    logger.info(f"Sent joke: '{d_joke['joke']}'")
    if response:
        jokes.put_sent_joke_db(conn, d_joke["id"], sent_from="twitter")
        logger.info("Joke sent via mail with joke_id='{}'".format(d_joke["id"]))
    else:
        logger.error("Joke not sent! joke_id='{}'".format(d_joke["id"]))
    return response
