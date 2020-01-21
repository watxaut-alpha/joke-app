import os

try:
    os.chdir(r"src/api")
except FileNotFoundError:
    os.chdir(r"../src/api")

from datetime import timedelta
from unittest.mock import patch
from starlette.testclient import TestClient
from passlib.context import CryptContext

from src.api.main import app
import src.api.src.auth.core as api_auth
from src.api.src.config import DOCS_USER, DOCS_PASSWORD

client = TestClient(app)


def get_oauth_password():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return api_auth.get_password_hash(pwd_context, DOCS_PASSWORD)


def get_oauth_token():
    access_token_expires = timedelta(minutes=api_auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = api_auth.create_access_token(data={"sub": DOCS_USER}, expires_delta=access_token_expires)
    return access_token


# Test main GET "/"
def test_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "<html>" in response.text
    assert "thecatapi.com" in response.text


# Test 404 template
def test_404():
    response = client.get("/asdf")
    assert response.status_code == 404
    assert "santajoan.jpg" in response.text
    assert "congrats" in response.text


# Test POST /user/telegram/add for success add
def test_add_user_telegram_success():
    with patch("src.api.src.db.users.has_db_telegram_user") as has_db_telegram_user:
        with patch("src.api.src.db.core.add_record") as add_record:
            has_db_telegram_user.return_value = False
            add_record.return_value = True

            url = "/users/telegram/add"
            user_id = 666623826648
            first_name = "Joan de las nieves"
            data = {"user_id": str(user_id), "first_name": first_name}
            token = get_oauth_token()
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Bearer {token}".format(token=token.decode("utf-8")),
            }
            response = client.post(url, json=data, headers=headers)

            assert response.status_code == 201
            assert "user_id" in response.json().keys()
            assert "first_name" in response.json().keys()


# "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
# "eyJzdWIiOiJ3YXR4YXV0IiwiZXhwIjoxNTcyNDYxNzk2fQ.8g1FZ_1_q - nW1BpElO1hv0Di10DeeQdnND0kfV - YmVY",

# user_id = 666623826648
# first_name = "Joan de las nieves"
# data = {"user_id": str(user_id), "first_name": first_name}
# token = get_oauth_token()
# headers = {
#     "Content-Type": "application/json",
#     # "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9."
#     "eyJzdWIiOiJ3YXR4YXV0IiwiZXhwIjoxNTcyNDYxNzk2fQ.8g1FZ_1_q - nW1BpElO1hv0Di10DeeQdnND0kfV - YmVY",
#     "Authorization": "Bearer {token}".format(token=token.decode("utf-8")),
# }
# print(headers)
