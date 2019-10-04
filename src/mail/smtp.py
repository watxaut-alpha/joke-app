import smtplib
import logging
import traceback

from email.mime.multipart import MIMEMultipart

from src.mail.secret import PASSWORD


def send_mail(mail_user: str, receivers: list, message: MIMEMultipart, email_text: str):
    logger = logging.getLogger("jokeBot")
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(mail_user, PASSWORD)

        server.sendmail(mail_user, receivers, message.as_string())
        server.close()

        logger.info('Email sent!: "{}"'.format(email_text))

        return True
    except:
        logger.error("Something went wrong sending the mail: '{}'".format(traceback.format_exc()))

        return False
