import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Bot, Update

import src.api as api

logger = logging.getLogger(__name__)

TIMEOUT_MSG = "Oops, something went wrong with the API. Try again later"


def start(bot: Bot, update: Update) -> None:
    logger.info('Command start issued')

    # get user info coming from telegram message
    user_id = str(update.message.chat.id)
    first_name = update.message.chat.first_name

    # add user to DB
    response = api.add_user_telegram(user_id, first_name)

    # send telegram message
    bot_message = """Hey newcomer! This bot is able to send bad jokes (in spanish for the moment). You have 3 options:
    - /send_joke -> which will send a random joke from the DB
    - /rate_joke -> which sends a joke and let's you rate it
    - /validate_joke -> sends a wannabe joke asking if it should be part of the 'curated list' of jokes
    
    Have fun!
    """
    bot.send_message(
        chat_id=update.message.chat_id,
        text=bot_message
    )


def send_joke(bot: Bot, update: Update) -> None:

    logger.info('Command send_joke issued')

    # query random joke from API
    response = api.get_random_joke()
    if response:
        str_joke = response.json()["joke"]
    else:
        str_joke = "Oops, something went wrong. Try again later"

    bot.send_message(
        chat_id=update.message.chat_id,
        text=str_joke
    )


def rate_joke(bot: Bot, update: Update) -> None:
    logger.info('Command rate_joke issued')

    # query random joke from API
    response = api.get_random_joke()
    if response:
        str_joke = response.json()["joke"]
        id_joke = response.json()["joke_id"]
    else:
        str_joke = TIMEOUT_MSG
        id_joke = -1

    bot.send_message(
        chat_id=update.message.chat_id,
        text=str_joke
    )

    # ratings
    s_ratings = "id: {id_joke} - How would you rate this joke?".format(id_joke=id_joke)

    keyboard = [[InlineKeyboardButton("0", callback_data=0),
                 InlineKeyboardButton("2.5", callback_data=2.5),
                 InlineKeyboardButton("5", callback_data=5),
                 InlineKeyboardButton("7.5", callback_data=7.5),
                 InlineKeyboardButton("10", callback_data=10)]]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(s_ratings, reply_markup=reply_markup)


def button_rating(bot: Bot, update: Update) -> None:

    chat_id = update.callback_query.message.chat_id
    message_id = update.callback_query.message["message_id"]
    user_id = update.callback_query.from_user.id
    bot_message = update.callback_query.message.text
    user_response = update.callback_query.data

    # TODO: I dont like this approach, there should be another..
    if "rate" in bot_message:

        new_text = "Thanks for rating! :)))"

        f_rating = float(user_response)

        # erase and get id "id: {id} - sdmcsdcma"
        joke_id = int(bot_message[4:].split(" - ")[0])

        request = api.insert_rating_joke(user_id, joke_id, f_rating)

    elif "joke" in bot_message:
        new_text = "Thanks for the feedback! :DD"

        is_joke = "1" == user_response

        # erase and get id "id: {id} - sdmcsdcma"
        validated_joke_id = int(bot_message[4:].split(" - ")[0])

        request = api.update_joke_validation(validated_joke_id, user_id, is_joke)
    else:
        new_text = "Thanks for the feedback brah! :DD"

    bot.editMessageText(new_text, chat_id=chat_id, message_id=message_id)


def validate_joke(bot: Bot, update: Update) -> None:
    logger.info('Command validate_joke issued')

    # query random joke and return only one in a pandas DF
    response = api.get_random_twitter_joke()

    if response:
        # unpack joke info and send it to telegram
        str_joke = response.json()["joke"]
        id_joke = response.json()["joke_id"]

        if id_joke == -1:  # API connects but no more jokes to validate

            bot.send_message(
                chat_id=update.message.chat_id,
                text="Whoops! No more jokes to validate"
            )
            return

        # else send message
        bot.send_message(
            chat_id=update.message.chat_id,
            text=str_joke
        )
        # ratings
        s_ratings = "id: {id_joke} - Is this even a joke?".format(id_joke=id_joke)

        keyboard = [[InlineKeyboardButton("Yep", callback_data=1),
                     InlineKeyboardButton("Nope", callback_data=0)]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_text(s_ratings, reply_markup=reply_markup)

    else:  # the table of twitter jokes is already all validated

        bot.send_message(
            chat_id=update.message.chat_id,
            text=TIMEOUT_MSG
        )
