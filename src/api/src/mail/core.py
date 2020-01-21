import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pathlib import Path

import time
from jinja2 import Template

import src.helpers as helpers
import src.mail.smtp as smtp
from src.config import HOST

logger = logging.getLogger("jokeApi")


def create_message_subscribed(mail_user: str, email_subscribed: str):
    subject = "One subscriber, one happy cat"

    email_text = """From: {from_mail}
    To: {to}
    Subject: {subject}
    {body}
    """.format(
        from_mail=mail_user, to=email_subscribed, subject=subject, body=""
    )
    parent_path = Path(__file__).resolve().parent

    # load mail template for ratings
    with open("{}/templates/thanks_subscribed.html".format(parent_path), "r") as f_subscribed:
        s_html = f_subscribed.read()

    # add params with jinja2 and the html
    rating_template = Template(s_html)
    email_html = rating_template.render(url=helpers.get_cat_url())

    # fancy email with html
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = mail_user
    message["To"] = email_subscribed

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(email_text, "plain")
    part2 = MIMEText(email_html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


def create_message_joke(mail_user: str, d_receiver: dict, d_joke: dict):
    signature = "Un pogramador que come zanahorias"
    disclaimer = """DISCLAIMER: THIS JOKE OR PROSA POETICA IS PROVIDED AS IS WITHOUT WARRANTY OF DELIVERING THE JOKE
    EVERYDAY, BREAKING THE CODE, BREAKING YOUR COMPUTER OR STARTING WW3. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
    HOLDERS BE ACCUSED OF RACISM, BAD JOKES OR 'THIS JOKE GAVE ME AIDS'. TALK TO MY HAND"""

    subject = "CHISTE MALO DEL DÍA - NINI EDITION: RELOADED"

    email_text = """From: {}
To: {}
Subject: {}
{}
{}""".format(
        mail_user, d_receiver["email"], subject, d_joke["joke"], disclaimer
    )

    # load mail template for ratings
    parent_path = Path(__file__).resolve().parent
    with open("{}/templates/mail_joke.html".format(parent_path), "r") as f_rating:
        s_html = f_rating.read()

    # add params with jinja2 and the html
    rating_template = Template(s_html)
    email_html = rating_template.render(
        joke=d_joke["joke"],
        host=HOST,
        joke_id=d_joke["id"],
        id_hash=d_receiver["id_hash"],
        signature=signature,
        disclaimer=disclaimer,
    )

    # fancy email with html
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = mail_user
    message["To"] = d_receiver["email"]

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(email_text, "plain")
    part2 = MIMEText(email_html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message


def send_subscribed_mail(mail_user: str, mail_pwd: str, email_subscribed: str):
    message = create_message_subscribed(mail_user, email_subscribed)
    is_sent = smtp.send_mail(mail_user, mail_pwd, email_subscribed, message)
    if not is_sent:
        logger.error("Something wrong with sending mail, mail not sent")
    return is_sent


def send_joke_mails(mail_user: str, mail_pwd: str, d_receivers: dict, d_joke: dict, provider: str = "smtp"):

    for d_receiver in d_receivers.values():
        message = create_message_joke(mail_user, d_receiver, d_joke)

        if provider == "smtp":

            is_sent = smtp.send_mail(mail_user, mail_pwd, d_receiver["email"], message)
            if not is_sent:
                logger.error("Something wrong with sending mail, mail not sent")
            time.sleep(1)

        else:
            raise Exception("Invalid provider. Must be one of ['smtp']")

    return True
