import pickle
import logging
import os.path

from apiclient import errors
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

logger = logging.getLogger("jokeBot")


def init_service():
    credentials = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    pickle_path = "src/mail/google/token.pickle"
    credentials_path = 'src/mail/google/credentials.json'

    if os.path.exists(pickle_path):
        with open(pickle_path, 'rb') as token:
            credentials = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(pickle_path, 'wb') as token:
            pickle.dump(credentials, token)

    service = build('gmail', 'v1', credentials=credentials)

    return service


def send_message(service, user_id, message):
    """Send an email message.

    Args:
      service: Authorized Gmail API service instance.
      user_id: User's email address. The special value "me"
      can be used to indicate the authenticated user.
      message: Message to be sent.

    Returns:
      Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
                   .execute())
        logger.info('Message Id: %s' % message['id'])
        return True
    except errors.HttpError as error:
        logger.error('An error occurred: %s' % error)
        return False
