import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import src.mail.google.google as gmail
import src.mail.smtp as smtp

SIGNATURE = "Fdo.: un pogramador que come zanahorias pero esta vez desde su puta casa y mucho mejor."
DISCLAIMER = """DISCLAIMER: THIS JOKE OR PROSA POETICA IS PROVIDED AS IS WITHOUT WARRANTY OF DELIVERING THE JOKE 
EVERYDAY, BREAKING THE CODE, BREAKING YOUR COMPUTER OR STARTING WW3. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
BE ACCUSED OF RACISM, BAD JOKES OR 'THIS JOKE GAVE ME AIDS'. TALK TO MY HAND"""

RECEIVERS = ["watxaut.alpha@gmail.com", ]

SUBJECT = "CHISTE MALO DEL DÍA - NINI EDITION: RELOADED"


def create_message(mail_user: str, receivers: list, joke: str, subject: str, signature: str, disclaimer: str):
    email_text = """From: {}
To: {}
Subject: {}
{}
{}""".format(mail_user, ",".join(receivers), subject, joke, disclaimer)

    email_html = """<html>
  <body>
    <br>
    <blockquote>
    <p>{joke}</p>
    </blockquote>
    <br>
    <p>{signature}</p>
    <hr>
    <p><sub>{disclaimer}</sub></p>
  </body>
</html>
""".format(joke=joke, signature=signature, disclaimer=disclaimer)

    # fancy email with html
    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = mail_user
    message["To"] = ",".join(receivers)

    # Turn these into plain/html MIMEText objects
    part1 = MIMEText(email_text, "plain")
    part2 = MIMEText(email_html, "html")

    # Add HTML/plain-text parts to MIMEMultipart message
    # The email client will try to render the last part first
    message.attach(part1)
    message.attach(part2)
    return message, email_text


def send_mail(mail_user: str, receivers: list, joke: str, subject: str, provider: str = "google"):
    message, email_text = create_message(mail_user, receivers, joke, subject, SIGNATURE, DISCLAIMER)

    if provider == "google":

        # init service
        service = gmail.init_service()

        message_raw = {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}
        is_sent = gmail.send_message(service, mail_user, message_raw)

    elif provider == "smtp":

        is_sent = smtp.send_mail(mail_user, receivers, message, email_text)

    else:
        raise Exception("Invalid provider. Must be one of ['google', 'smtp']")

    return is_sent
