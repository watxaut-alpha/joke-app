import requests
import datetime
from fastapi import FastAPI
from pydantic import BaseModel
from starlette.requests import Request
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

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
    source: str


class UserValidation(BaseModel):
    joke_id: int
    user_id: str
    is_joke: bool


class UserTag(BaseModel):
    joke_id: int
    user_id: str
    tag_id: int


@app.get("/")
async def main(request: Request):

    r_cat = requests.get("https://api.thecatapi.com/v1/images/search")
    if r_cat:  # status 200
        url = r_cat.json()[0]["url"]
    else:
        url = "Cat not found"

    return templates.TemplateResponse("index.html", {"request": request, "url": url})


@app.exception_handler(404)
async def not_found(request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)


@app.get("/legal/")
async def legal(request: Request):
    return templates.TemplateResponse("legal.html", {"request": request})


@app.post("/user/telegram/add", status_code=201)
async def add_user(user: TelegramUser):
    users.add_user_telegram(user.user_id, user.first_name)
    return user


@app.post("/user/mail/add", status_code=201)
async def add_mail_user(user: MailUser):
    users.add_user_mail(user.email)
    return user


@app.get("/jokes/random")
async def send_random_joke():
    df = jokes.get_random_joke()
    response = {"joke_id": int(df["id"][0]), "joke": df["joke"][0]}
    return response


@app.get("/jokes/rating/{joke_id}/{id_hash}/{rating}")
async def joke_rating(request: Request, joke_id: int, id_hash: str, rating: float):

    if 0 <= rating <= 10:
        jokes.upsert_rating_joke(id_hash, joke_id, rating, "mail")
        t = datetime.datetime.now()
        d = t.day
        m = t.month
        if id_hash == "cef6b0a6-ef4e-11e9-823c-0242ac150002" and d == 23 and m == 10:
            # troll jaime
            return templates.TemplateResponse("troll_jaime.html", {"request": request, "rating": rating})
        else:
            return templates.TemplateResponse("thanks_rating.html", {"request": request, "rating": rating})
    else:
        reason = "Your rating is invalid, like Clarita"
        return templates.TemplateResponse("nope.html", {"request": request, "reason": reason})


# define the same method but with put
@app.put("/jokes/rating")
async def joke_rating_put(user_rating: UserRating):
    jokes.upsert_rating_joke(**user_rating.dict())
    return {"message": "success"}


@app.put("/jokes/validate")
async def update_joke_validation(user_validation: UserValidation):
    validation.update_joke_validation(**user_validation.dict())
    return {"message": "success"}


@app.get("/jokes/tags")
async def get_tags():
    l_tags = jokes.get_tags()
    return {"tags": l_tags}


@app.put("/jokes/tag")
async def tag_joke(user_tag: UserTag):
    jokes.upsert_joke_tag(**user_tag.dict())
    return {"message": "success"}


@app.get("/jokes/tags/random")
async def get_untagged_joke():
    df = jokes.get_untagged_joke()
    if not df.empty:
        response = {"joke": df["joke"][0], "joke_id": int(df["id"][0])}
    else:
        response = {"joke": "No more jokes to tag", "joke_id": -1}
    return response


@app.get("/jokes/validate/random")
async def get_random_validate_joke():
    df = validation.get_random_twitter_joke()
    if not df.empty:
        response = {"joke": df["joke"][0], "joke_id": int(df["id"][0])}
    else:
        response = {"joke": "No more jokes to validate", "joke_id": -1}
    return response
