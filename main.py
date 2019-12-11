import argparse
import logging
import os

import src.tasks.send as tasks
import src.tasks.validate as validate


if __name__ == "__main__":

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger("jokeBot")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--action",
        type=str,
        choices=["send_joke_mail", "validate_jokes", "tweet_joke"],
        help="Type of action to run. Leave empty to run the bot",
    )

    parser.add_argument("-d", "--debug", action="store_true", help="Does whatever with debug params")

    args = parser.parse_args()

    # change dir to current main.py (when executed in cron)
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    if args.action == "send_joke_mail":
        tasks.send_mail(args.debug)
    elif args.action == "validate_jokes":
        validate.put_validated_jokes_in_joke_db()
    elif args.action == "tweet_joke":
        tasks.send_tweet()
    else:
        raise Exception("Option for action not recognized: '{}'".format(args.action))
