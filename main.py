import logging
import argparse

import src.bot.start as bot
import src.tasks.mail as mail
import src.tasks.validate as validate

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=str, choices=['send_joke_mail', "validate_jokes"],
                        help="Type of action to run. Leave empty to run the bot")

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('jokeBot')

    if parser.action is None:

        # starts the telegram bot and adds the dispatcher for the functions
        bot.start_bot()

    elif parser.action == "send_joke_mail":
        mail.send_mail()

    elif parser.action == "validate_jokes":
        validate.put_validated_jokes_in_joke_db()

    else:
        raise Exception("Option for action not recognized: '{}'".format(parser.action))

