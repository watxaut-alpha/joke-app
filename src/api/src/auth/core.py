import datetime
from datetime import timedelta

import jwt
from pydantic import BaseModel

import src.db.users as users
from src.auth.secret import ALGORITHM, SECRET_KEY

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str = None


class User(BaseModel):
    id: int
    username: str
    email: str
    disabled: bool
    scopes: str = None


class UserInDB(User):
    hashed_password: str


def get_user(username: str):
    df = users.get_admin_users()
    if username in df["username"].values:
        df = df[df["username"] == username]
        user_dict = df.to_dict(orient="index")[0]
        return UserInDB(**user_dict)


def authenticate_user(pwd_context, username: str, password: str):
    user = get_user(username)
    if not user:
        return False
    if not verify_password(pwd_context, password, user.hashed_password):
        return False
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(pwd_context, password):
    return pwd_context.hash(password)


def verify_password(pwd_context, plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)