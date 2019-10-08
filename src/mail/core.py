from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template

import src.mail.smtp as smtp

SIGNATURE = "Fdo.: un pogramador que come zanahorias pero esta vez desde su puta casa y mucho mejor."
DISCLAIMER = """DISCLAIMER: THIS JOKE OR PROSA POETICA IS PROVIDED AS IS WITHOUT WARRANTY OF DELIVERING THE JOKE 
EVERYDAY, BREAKING THE CODE, BREAKING YOUR COMPUTER OR STARTING WW3. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE ACCUSED OF RACISM, BAD JOKES OR 'THIS JOKE GAVE ME AIDS'. TALK TO MY HAND"""

RECEIVERS = ["watxaut.alpha@gmail.com", ]

SUBJECT = "CHISTE MALO DEL DÍA - NINI EDITION: RELOADED"


def create_message(mail_user: str, d_receiver: dict, d_joke: dict, subject: str, signature: str, disclaimer: str):
    email_text = """From: {}
To: {}
Subject: {}
{}
{}""".format(mail_user, d_receiver["email"], subject, d_joke["joke"], disclaimer)

    # load mail template for ratings
    with open("src/mail/templates/rating.html", "r") as f_rating:
        s_html = f_rating.read()

    rating_template = Template(s_html)
    email_html = rating_template.render(
        joke=d_joke["joke"],
        joke_id=d_joke["id"],
        id_hash=d_receiver["id_hash"],
        signature=signature,
        disclaimer=disclaimer
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


def send_mail(mail_user: str, mail_pwd: str, d_receivers: dict, d_joke: dict, subject: str, provider: str = "smtp"):

    for d_receiver in d_receivers.values():
        message = create_message(mail_user, d_receiver, d_joke, subject, SIGNATURE, DISCLAIMER)

        if provider == "smtp":

            is_sent = smtp.send_mail(mail_user, mail_pwd, d_receiver["email"], message)

        else:
            raise Exception("Invalid provider. Must be one of ['smtp']")

    return True
