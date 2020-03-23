import os

import dotenv
import requests

dotenv.load_dotenv(r"../../config/env-api.env")


def get_token_from_api():
    oauth_docs_user = os.getenv("OAUTH_DOCS_USER")
    oauth_docs_pwd = os.getenv("OAUTH_DOCS_PWD")

    url = "https://watxaut.com/api/v1/token"
    params = {"username": oauth_docs_user, "password": oauth_docs_pwd}
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url=url, data=params, headers=headers)
    return r.json()["access_token"]


def send_joke_from_api():
    url = "https://watxaut.com/api/v1/jokes/send"
    token = get_token_from_api()
    headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    r = requests.post(url, headers=headers)
    if r:
        return True
    else:
        return False


send_joke_from_api()
