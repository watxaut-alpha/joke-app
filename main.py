import argparse
import logging

import src.bot.start as bot
import src.tasks.mail as mail
import src.tasks.validate as validate

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('jokeBot')

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=str, choices=['send_joke_mail', "validate_jokes"],
                        help="Type of action to run. Leave empty to run the bot")

    args = parser.parse_args()

    if args.action is None:

        # starts the telegram bot and adds the dispatcher for the functions
        bot.start_bot()

    elif args.action == "send_joke_mail":
        mail.send_mail()

    elif args.action == "validate_jokes":
        validate.put_validated_jokes_in_joke_db()

    else:
        raise Exception("Option for action not recognized: '{}'".format(args.action))
