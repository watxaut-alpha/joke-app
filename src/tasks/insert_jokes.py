import os

import dotenv
import pytesseract
import requests
from PIL import Image

dotenv.load_dotenv(r"../../config/env-api.env")


def get_token_from_api():
    oauth_docs_user = os.getenv("OAUTH_DOCS_USER")
    oauth_docs_pwd = os.getenv("OAUTH_DOCS_PWD")

    url = "https://watxaut.com/api/v1/token"
    params = {"username": oauth_docs_user, "password": oauth_docs_pwd}
    headers = {"accept": "application/json", "Content-Type": "application/x-www-form-urlencoded"}
    r = requests.post(url=url, data=params, headers=headers)
    return r.json()["access_token"]


def add_joke_from_api(jokes: list, author: str, author_mail: str = None):
    url = "https://watxaut.com/api/v1/jokes/add"
    token = get_token_from_api()
    headers = {"accept": "application/json", "Content-Type": "application/json", "Authorization": f"Bearer {token}"}
    for joke in jokes:
        if not author_mail:
            data = {"joke": joke, "author": author}
        else:
            data = {"joke": joke, "author": author, "author_mail": author_mail}
        r = requests.post(url, json=data, headers=headers)
        if not r:
            raise Exception(f"Error with adding joke: {r.text}")
    return True


def read_img_joke(img):
    joke_text = pytesseract.image_to_string(Image.open(img))
    return joke_text
