import smtplib
import logging
import traceback

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger("jokeBot")

DISCLAIMER = """Fdo.: un pogramador que come zanahorias pero esta vez desde su puta casa y mucho mejor.

------------------------------------------------------------
DISCLAIMER: THIS JOKE OR PROSA POETICA IS PROVIDED AS IS WITHOUT WARRANTY OF DELIVERING THE JOKE EVERYDAY, 
BREAKING THE CODE, BREAKING YOUR COMPUTER OR STARTING WW3. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE 
ACCUSED OF RACISM, BAD JOKES OR 'THIS JOKE GAVE ME AIDS'. TALK TO MY HAND"""

RECEIVERS = ["watxaut.alpha@gmail.com", ]

SUBJECT = "CHISTE MALO DEL DÍA - NINI EDITION: RELOADED"


def send_mail(mail_user: str, mail_pwd: str, receivers: list, joke: str, subject: str, disclaimer: str):

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
    <p><sub>{disclaimer}</sub></p>
  </body>
</html>
""".format(joke=joke, disclaimer=disclaimer)

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

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(mail_user, mail_pwd)

        server.sendmail(mail_user, receivers, message.as_string())
        server.close()

        logger.info('Email sent!: "{}"'.format(email_text))

    except:
        logger.error("Something went wrong sending the mail: '{}'".format(traceback.format_exc()))
        return False

    return True


# from src.mail.secret import USER, PASSWORD
# send_mail(USER, PASSWORD, [USER,], "THIS IS A JOKE MAN", "Prova html", "This is a disclaimer")
