import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

import src.db.core as db
import src.db.helpers as db_helpers
import src.db.users as users
import src.db.constants as db_ct
import src.db.jokes as jokes
import src.db.twitter as twitter_db

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


def button_rating(bot, update):

    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message["message_id"]
    user_id = update.callback_query.from_user.id
    bot_message = update.callback_query.message.text
    user_response = update.callback_query.data

    conn = db.get_jokes_app_connection()

    # TODO: I dont like this approach, there should be another..
    if "rate" in bot_message:

        new_text = "Thanks for rating! :)))"

        f_rating = float(user_response)

        # erase and get id "id: {id} - sdmcsdcma"
        joke_id = int(bot_message[4:].split(" - ")[0])

        jokes.insert_rating_joke(conn, user_id, joke_id, f_rating)

    elif "joke" in bot_message:
        new_text = "Thanks for the feedback! :DD"

        is_joke = "1" == user_response

        # erase and get id "id: {id} - sdmcsdcma"
        tweet_str_id = int(bot_message[4:].split(" - ")[0])

        twitter_db.update_joke_validation(conn, tweet_str_id, user_id, is_joke)
    else:
        new_text = "Thanks for the feedback brah! :DD"

    bot.editMessageText(new_text, chat_id=chat_id, message_id=message_id)


def validate_joke(bot, update):
    logger.info('Command validate_joke issued')

    # get user info coming from telegram message
    user_id = update.message.chat.id
    first_name = update.message.chat.first_name
    message = update.message.text

    # instance connection to PSQL DB
    conn = db.get_jokes_app_connection()

    # add log
    db_helpers.add_telegram_log(conn, db_ct.USER, message, user_id, "name", first_name)

    # query random joke and return only one in a pandas DF
    df = twitter_db.get_random_twitter_joke(conn)

    # unpack joke info and send it to telegram
    str_joke = df["joke"][0]
    id_joke = df["id"][0]

    bot.send_message(
        chat_id=update.message.chat_id,
        text=str_joke
    )

    db_helpers.add_telegram_log(conn, db_ct.BOT, message, user_id, "twitter_joke_id", id_joke)

    # ratings
    s_ratings = "id: {id_joke} - Is this even a joke?".format(id_joke=id_joke)

    keyboard = [[InlineKeyboardButton("Yep", callback_data=1),
                 InlineKeyboardButton("Nope", callback_data=0)]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(s_ratings, reply_markup=reply_markup)

    conn = None
