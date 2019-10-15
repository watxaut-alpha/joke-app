import requests

from requests.exceptions import Timeout

from src.secret import HOST, PORT

TIMEOUT = 1.5  # secs


def connect(func):

    def f(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Timeout:
            return False

    return f


@connect
def add_user_telegram(user_id: str, first_name: str) -> requests.Response:
    url = "{host}:{port}/user/add".format(host=HOST, port=PORT)
    data = {
        'user_id': str(user_id),
        'first_name': first_name
    }
    return requests.post(url, json=data, timeout=TIMEOUT)


@connect
def get_random_joke() -> requests.Response:
    url = "{host}:{port}/jokes/random".format(host=HOST, port=PORT)
    return requests.get(url, timeout=TIMEOUT)


@connect
def insert_rating_joke(user_id: str, joke_id: int, f_rating: float) -> requests.Response:
    url = "{host}:{port}/jokes/rating".format(host=HOST, port=PORT)
    data = {
        'user_id': user_id,
        'joke_id': joke_id,
        'rating': f_rating
    }
    return requests.put(url, json=data, timeout=TIMEOUT)


@connect
def update_joke_validation(validated_joke_id: int, user_id: str, is_joke: bool) -> requests.Response:
    url = "{host}:{port}/jokes/validate".format(host=HOST, port=PORT)
    data = {
        'joke_id': validated_joke_id,
        'user_id': user_id,
        'is_joke': is_joke
    }
    return requests.put(url, json=data, timeout=TIMEOUT)


@connect
def get_random_twitter_joke() -> requests.Response:
    url = "{host}:{port}/jokes/validate/random".format(host=HOST, port=PORT)
    return requests.get(url, timeout=TIMEOUT)
