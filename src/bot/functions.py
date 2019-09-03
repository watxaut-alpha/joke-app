import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

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

    # ratings
    s_ratings = "id: {id_joke} - How would you rate this joke?".format(id_joke=id_joke)

    keyboard = [[InlineKeyboardButton("0", callback_data=0),
                 InlineKeyboardButton("2.5", callback_data=2.5),
                 InlineKeyboardButton("5", callback_data=5),
                 InlineKeyboardButton("7.5", callback_data=7.5),
                 InlineKeyboardButton("10", callback_data=10)]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(s_ratings, reply_markup=reply_markup)

    conn = None

    return id_joke


def button_rating(bot, update):

    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message["message_id"]
    new_text = "Thanks for rating! :)))"

    bot.editMessageText(new_text, chat_id=chat_id, message_id=message_id)

    conn = db.get_jokes_app_connection()

    user_id = update.callback_query.from_user.id
    joke_id = update.callback_query.message.text
    f_rating = float(update.callback_query.data)

    # erase and get id "id: {id} - sdmcsdcma"
    joke_id = int(joke_id[4:].split(" - ")[0])

    jokes.insert_rating_joke(conn, user_id, joke_id, f_rating)
