from pydantic import BaseModel


class UserRating(BaseModel):
    user_id: str
    joke_id: int
    rating: float
    source: str


class TelegramUser(BaseModel):
    user_id: str
    first_name: str


class MailUser(BaseModel):
    email: str


class UserValidation(BaseModel):
    joke_id: int
    user_id: str
    is_joke: bool


class UserJoke(BaseModel):
    joke: str
    author: str


class UserTag(BaseModel):
    joke_id: int
    user_id: str
    tag_id: int
