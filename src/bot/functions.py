import logging

import src.db.core as db
import src.db.helpers as db_helpers
import src.db.users as users
import src.db.constants as db_ct
import src.db.jokes as jokes

logger = logging.getLogger('jokeBot')


def start(bot, update):
    logger.info('Command start issued')

    # get user info coming from telegram message
    user_id = update.message.chat.id
    first_name = update.message.chat.first_name
    message = update.message.text

    # instance connection to PSQL DB
    conn = db.get_jokes_app_connection()

    # add log
    db_helpers.add_telegram_log(conn, db_ct.USER, message, user_id, "name", first_name)

    # add user to DB
    users.add_user(conn, user_id, first_name)

    # send telegram message
    bot_message = "Hey hey, new chistes everyday"
    bot.send_message(
        chat_id=update.message.chat_id,
        text=bot_message
    )

    # add log
    db_helpers.add_telegram_log(conn, db_ct.BOT, bot_message, user_id, "name", first_name)

    conn = None


def send_joke(bot, update):
    logger.info('Command send_joke issued')

    # get user info coming from telegram message
    user_id = update.message.chat.id
    first_name = update.message.chat.first_name
    message = update.message.text

    # instance connection to PSQL DB
    conn = db.get_jokes_app_connection()

    # add log
    db_helpers.add_telegram_log(conn, db_ct.USER, message, user_id, "name", first_name)

    # query random joke and return only one in a pandas DF
    df = jokes.get_random_joke(conn)

    # unpack joke info and send it to telegram
    str_joke = df["joke"][0]
    id_joke = df["id"][0]

    bot.send_message(
        chat_id=update.message.chat_id,
        text=str_joke
    )

    db_helpers.add_telegram_log(conn, db_ct.BOT, message, user_id, "joke_id", id_joke)

    conn = None


def step_rating_joke(message):
    cid = message.chat.id
    rating = message.text
    print(cid, rating)


def button(bot, update):
    query = update.callback_query

    print(query.data)
