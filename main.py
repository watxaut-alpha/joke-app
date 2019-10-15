import argparse
import logging

import src.tasks.send as mail
import src.tasks.validate as validate

if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger('jokeBot')

    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--action", type=str, choices=['send_joke_mail', "validate_jokes", "start_server"],
                        help="Type of action to run. Leave empty to run the bot")

    args = parser.parse_args()

    if args.action == "send_joke_mail":
        mail.send_mail()

    elif args.action == "validate_jokes":
        validate.put_validated_jokes_in_joke_db()

    else:
        raise Exception("Option for action not recognized: '{}'".format(args.action))
