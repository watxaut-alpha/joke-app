import requests

from fastapi import FastAPI
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates
from pydantic import BaseModel

import src.db.jokes as jokes
import src.db.users as users
import src.db.validation as validation

# uvicorn main:app --host 0.0.0.0 --port 8080
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


class TelegramUser(BaseModel):
    user_id: str
    first_name: str


class MailUser(BaseModel):
    email: str


class UserRating(BaseModel):
    user_id: str
    joke_id: int
    rating: float


class UserValidation(BaseModel):
    joke_id: int
    user_id: str
    is_joke: bool


@app.get("/")
async def main(request: Request):

    r_cat = requests.get("https://api.thecatapi.com/v1/images/search")
    if r_cat:  # status 200
        url = r_cat.json()[0]["url"]
    else:
        url = "Cat not found"

    return templates.TemplateResponse("index.html", {"request": request, "url": url})


@app.post("/user/telegram/add", status_code=201)
async def add_user(user: TelegramUser):
    users.add_user_telegram(user.user_id, user.first_name)
    return user


@app.post("/user/mail/add", status_code=201)
async def add_user(user: MailUser):
    users.add_user_mail(user.email)
    return user


@app.get("/jokes/random")
async def send_random_joke():
    df = jokes.get_random_joke()
    response = {
        "joke_id": int(df["id"][0]),
        "joke": df["joke"][0]
    }
    return response


@app.get("/jokes/rating/{joke_id}/{id_hash}/{rating}")
async def joke_rating(request: Request, joke_id: int, id_hash: str, rating: float):
    jokes.insert_rating_joke(id_hash, joke_id, rating)
    return templates.TemplateResponse("thanks_rating.html", {"request": request, "rating": rating})


# define the same method but with put
@app.put("/jokes/rating")
async def joke_rating_put(user_rating: UserRating):
    jokes.insert_rating_joke(**user_rating.dict())
    return {"message": "success"}


@app.put("/jokes/validate")
async def update_joke_validation(user_validation: UserValidation):
    validation.update_joke_validation(**user_validation.dict())
    return {"message": "success"}


@app.get("/jokes/validate/random")
async def get_random_validate_joke():
    df = validation.get_random_twitter_joke()
    if not df.empty:
        response = {
            "joke": df["joke"][0],
            "joke_id": int(df["id"][0])
        }
    else:
        response = {
            "joke": "No more jokes to validate",
            "joke_id": -1
        }
    return response
