import argparse
import logging
import os

import src.tasks.send as mail
import src.tasks.validate as validate
import src.tasks.notebooks as notebooks


if __name__ == "__main__":

    logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
    logger = logging.getLogger("jokeBot")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a",
        "--action",
        type=str,
        choices=["send_joke_mail", "validate_jokes", "export_jupyter"],
        help="Type of action to run. Leave empty to run the bot",
    )

    args = parser.parse_args()

    # change dir to current main.py (when executed in cron)
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
    os.chdir(dname)

    if args.action == "send_joke_mail":
        mail.send_mail()
    elif args.action == "validate_jokes":
        validate.put_validated_jokes_in_joke_db()
    elif args.action == "export_jupyter":
        notebooks.export_user_analysis()
    else:
        raise Exception("Option for action not recognized: '{}'".format(args.action))
