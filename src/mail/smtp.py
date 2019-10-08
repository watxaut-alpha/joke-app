import smtplib
import logging
import traceback

from email.mime.multipart import MIMEMultipart


def send_mail(mail_user: str, mail_pwd: str, receiver: str, message: MIMEMultipart):
    logger = logging.getLogger("jokeBot")
    try:
        if mail_user.endswith("gmail.com"):
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        elif mail_user.endswith("yahoo.com"):
            server = smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465)
        else:
            return False

        server.ehlo()
        server.login(mail_user, mail_pwd)

        server.sendmail(mail_user, receiver, message.as_bytes())

        server.close()

        logger.info('Email sent!: "{}"'.format(message.as_string()))

        return True
    except:
        logger.error("Something went wrong sending the mail: '{}'".format(traceback.format_exc()))

        return False
