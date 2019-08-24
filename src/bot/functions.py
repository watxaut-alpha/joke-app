import logging

import src.db.core as db
from src.db.secret import host, db_name, POSTGRES_PASSWORD, POSTGRES_USER

logger = logging.getLogger('jokeBot')


def start(bot, update):
    logger.info('Command start issued')
    bot.send_message(
        chat_id=update.message.chat_id,
        text="Hey hey, new chistes everyday"
    )


def send_joke(bot, update):
    logger.info('Command send_joke issued')

    # get sqlalchemy postgres connection
    conn = db.connect(host, POSTGRES_USER, POSTGRES_PASSWORD, db_name)

    # query new joke
    sql = "SELECT * FROM jokes ORDER BY random() LIMIT 1;"

    str_joke = db.execute_query(conn, sql)["joke"][0]

    bot.send_message(
        chat_id=update.message.chat_id,
        text=str_joke
    )

    conn = None
