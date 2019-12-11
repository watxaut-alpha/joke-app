import requests

from requests.exceptions import Timeout

from src.secret import HOST

API_V_STR: str = "/api/v1"
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
    url = f"{HOST}{API_V_STR}/users/telegram/add"
    data = {"user_id": str(user_id), "first_name": first_name}
    return requests.post(url, json=data, timeout=TIMEOUT)


@connect
def get_random_joke() -> requests.Response:
    url = f"{HOST}{API_V_STR}/jokes/random"
    return requests.get(url, timeout=TIMEOUT)


@connect
def insert_rating_joke(user_id: str, joke_id: int, f_rating: float) -> requests.Response:
    url = f"{HOST}{API_V_STR}/jokes/rating"
    data = {"user_id": user_id, "joke_id": joke_id, "rating": f_rating, "source": "telegram"}
    return requests.put(url, json=data, timeout=TIMEOUT)


@connect
def update_joke_validation(validated_joke_id: int, user_id: str, is_joke: bool) -> requests.Response:
    url = f"{HOST}{API_V_STR}/jokes/validate"
    data = {"joke_id": validated_joke_id, "user_id": str(user_id), "is_joke": is_joke}
    return requests.put(url, json=data, timeout=TIMEOUT)


@connect
def get_random_validation_joke() -> requests.Response:
    url = f"{HOST}{API_V_STR}/jokes/validate/random"
    return requests.get(url, timeout=TIMEOUT)


@connect
def get_untagged_joke() -> requests.Response:
    url = f"{HOST}{API_V_STR}/jokes/tags/random"
    return requests.get(url, timeout=TIMEOUT)


@connect
def get_tags() -> requests.Response:
    url = f"{HOST}{API_V_STR}/jokes/tags"
    return requests.get(url, timeout=TIMEOUT)


@connect
def tag_joke(joke_id, user_id, tag_id) -> requests.Response:
    url = f"{HOST}{API_V_STR}/jokes/tag"
    data = {"joke_id": joke_id, "user_id": user_id, "tag_id": tag_id}
    return requests.put(url, json=data, timeout=TIMEOUT)
