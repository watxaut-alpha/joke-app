from datetime import timedelta

import jwt
import requests
from fastapi import FastAPI, Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import PyJWTError
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.requests import Request
from starlette.responses import JSONResponse, FileResponse
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.templating import Jinja2Templates

try:
    import src.auth.core as auth
    import src.db.jokes as jokes
    import src.db.users as users
    import src.db.validation as validation
    from src.auth.secret import SECRET_KEY, ALGORITHM, DOCS_USER, DOCS_PASSWORD
except ModuleNotFoundError:
    import src.api.src.auth.core as auth
    import src.api.src.db.jokes as jokes
    import src.api.src.db.users as users
    import src.api.src.db.validation as validation
    from src.api.src.auth.secret import SECRET_KEY, ALGORITHM, DOCS_USER, DOCS_PASSWORD

# prod
# uvicorn main:app --host 0.0.0.0 --port 80
# Test
# uvicorn main:app --reload


title = "Jokes App API"
description = """This API is intended for creating an interface for jokes to be validated, tagged and sent to users.
You may need to authenticate if you plan on adding more users or doing sensible actions on endpoints that
erase/modify information in the DB"""

# Create FastApi app (has to be named like this) and set openAPI to None, we will set it later
# Define the paths for static and template paths, both relative to src/api
app = FastAPI(title=title, description=description, docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Creates a encryption context with Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
security = HTTPBasic()  # this one is only for /docs endpoint


# OAuth User login. Code gotten from https://fastapi.tiangolo.com/tutorial/security/intro/ and adapted for my app
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = auth.TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = auth.get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# OAuth User login. Code gotten from https://fastapi.tiangolo.com/tutorial/security/intro/ and adapted for my app
async def get_current_active_user(current_user: auth.User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


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


# OAuth User login. Code gotten from https://fastapi.tiangolo.com/tutorial/security/intro/ and adapted for my app
@app.post("/token", response_model=auth.Token, include_in_schema=False)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(pwd_context, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/", include_in_schema=False)
async def main(request: Request):
    """
    Main endpoint with no use at all, does not do very much. Shows an image of a cat using a free API.
    :param request: User GET Request
    :return: html with template index.html
    """

    r_cat = requests.get("https://api.thecatapi.com/v1/images/search")
    if r_cat:  # status 200
        url = r_cat.json()[0]["url"]
    else:
        url = "Cat not found"

    return templates.TemplateResponse("index.html", {"request": request, "url": url})


@app.exception_handler(404)
async def not_found(request, exc):
    return templates.TemplateResponse("fpqll.html", {"request": request}, status_code=404)


@app.get("/openapi.json", include_in_schema=False)
async def get_open_api_endpoint(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Returns the openapi.json schema if the credentials are matched, else shows 401
    :param credentials: credentials of the popup shown in the web page
    :return: Returns openAPI's json
    """
    if credentials.username != DOCS_USER or credentials.password != DOCS_PASSWORD:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return JSONResponse(get_openapi(title=title, version="v1", description=description, routes=app.routes))


@app.get("/docs", include_in_schema=False)
async def get_documentation(credentials: HTTPBasicCredentials = Depends(security)):
    """
    Returns the Swagger - openAPI page if the credentials in src/auth/secret.py are matched, else shows 401
    :param credentials: credentials of the popup shown in the web page
    :return: Returns the html template for openAPI's page
    """
    if credentials.username != DOCS_USER or credentials.password != DOCS_PASSWORD:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return get_swagger_ui_html(openapi_url="/openapi.json", title="{} Docs".format(title))


@app.get("/.well-known/acme-challenge/{file_name}", include_in_schema=False)
async def acme_challenge(file_name: str):
    file_path = "./.well-known/acme-challenge/{}".format(file_name)
    return FileResponse(file_path)


@app.get("/legal", include_in_schema=False)
async def legal(request: Request):
    """
    Shows the legal.html template with the legal agreement (for watxaut)
    :param request: User's GET Request
    :return: template with the html response
    """
    return templates.TemplateResponse("legal.html", {"request": request})


@app.get("/user/me")
async def read_users_me(current_user: auth.User = Depends(get_current_user)):
    """
    Gets the current logged via OAuth user information (in the model users_admin)
    :param current_user: Contains the user name, email, hashed password, disabled and scope information
    :return: returns current User
    """
    return current_user


@app.post("/user/telegram/add", status_code=201)
async def add_user(user: TelegramUser, current_user: auth.User = Depends(get_current_user)):
    """
    Adds a telegram user (the start function does so). Does not have much sense here, just for testing.
    Admin rights are needed for this one in order to keep the DB clean
    :param current_user: User model
    :param user: TelegramUser model
    :return: returns the created user
    """
    users.add_user_telegram(user.user_id, user.first_name)
    return user


@app.get("/user/mail/subscribe", status_code=200)
async def show_subscribe_page(request: Request):
    return templates.TemplateResponse("subscribe.html", {"request": request})


@app.post("/user/mail/add", status_code=201)
async def add_mail_user(request: Request):
    """
    Adds a user to the users_mail table. Every 8.30 (Spain Local Timezone) a cron sends a mail to every entry in the
    users_mail with a joke and the ability to rate it from the mail.
    :param request: Request object
    :return: returns a template
    """
    d_email = dict(await request.form())
    users.add_user_mail(d_email["email"])
    return templates.TemplateResponse("subscribed.html", {"request": request})


@app.get("/user/mail/unsubscribe", status_code=200)
async def show_unsubscribe_page(request: Request):
    return templates.TemplateResponse("unsubscribe.html", {"request": request})


@app.post("/user/mail/unsubscribed", status_code=201)
async def unsubscribe_from_mail(request: Request):
    """
    Removes user from the distribution mail list
    :param request: Request object
    :return: returns MailUser model
    """

    d_email = dict(await request.form())
    is_removed, msg = users.soft_delete_user_mail(d_email["email"])

    if is_removed:
        # return {"message": msg, "is_removed": is_removed}
        return templates.TemplateResponse("unsubscribed.html", {"request": request})
    else:
        return {"message": msg, "is_removed": is_removed}


@app.get("/jokes/random")
async def send_random_joke():
    """
    Gets a random joke from the jokes table (already validated)
    :return: json response = {joke_id, joke}
    """
    df = jokes.get_random_joke()
    response = {"joke_id": int(df["id"][0]), "joke": df["joke"][0]}
    return response


@app.get("/users")
async def get_all_users(current_user: auth.User = Depends(get_current_user)):
    d_users = users.get_users_mail().to_dict(orient="index")
    return d_users


@app.get("/jokes/rating/{joke_id}/{id_hash}/{rating}")
async def joke_rating(request: Request, joke_id: int, id_hash: str, rating: float):
    """
    Puts the rating into the ratings table for the joke with joke_id. The user's hash must exist
    in users table or in users_mail table.
    :param request: GET user Request
    :param joke_id: int representing the id of the joke in the jokes table
    :param id_hash: id hash representing user (telegram or mail user)
    :param rating: int in [0, 10]
    :return: returns template to show to user. If the rating is not correct or it times-out or the id does not
    exist, then it shows nope.html
    """

    if 0 <= rating <= 10:

        # try to add rating. If it gives false, be it connection with DB or false hash id return nope.html
        b_rating = jokes.upsert_rating_joke(id_hash, joke_id, rating, "mail")
        if b_rating:  # if everything goes OK
            template = templates.TemplateResponse("thanks_rating.html", {"request": request, "rating": rating})
        else:
            reason = (
                "Your rating is invalid, like Clarita. Reason: "
                "(Connection timeout, user ID not correct or joke id not in DB)"
            )
            template = templates.TemplateResponse("nope.html", {"request": request, "reason": reason})
    else:
        reason = "Your rating is invalid, like Clarita. Reason: rating not in [0, 10]"
        template = templates.TemplateResponse("nope.html", {"request": request, "reason": reason})

    return template


# define the same method but with put
@app.put("/jokes/rating")
async def joke_rating_put(user_rating: UserRating):
    """
    The same method as above, but with put so much more secure
    :param user_rating: UserRating Model
    :return: returns json with success or fail
    """
    b_rating = jokes.upsert_rating_joke(**user_rating.dict())
    if b_rating:
        return {"message": "success"}
    else:
        return {"message": "Error: timed-out, hash id not in DB or joke id not in DB"}


@app.put("/jokes/validate")
async def update_joke_validation(user_validation: UserValidation):
    """
    Jokes coming from scraped websites must be validated before going to jokes table, this function updates
    the validate_jokes table
    :param user_validation: UserValidation Model
    :return: json
    """
    validation.update_joke_validation(**user_validation.dict())
    return {"message": "success"}


@app.get("/jokes/tags")
async def get_tags():
    """
    Gets available tags for jokes from tags table
    :return: json = {tags: l_tags}
    """
    l_tags = jokes.get_tags()
    return {"tags": l_tags}


@app.put("/jokes/tag")
async def tag_joke(user_tag: UserTag):
    """
    Tags a joke from jokes table
    :param user_tag: UserTag Model
    :return: json
    """
    jokes.upsert_joke_tag(**user_tag.dict())
    return {"message": "success"}


@app.get("/jokes/tags/random")
async def get_untagged_joke():
    """
    Gets an untagged joke from the jokes table and sends returns it
    :return: json = {joke_id, joke}
    """
    df = jokes.get_untagged_joke()
    if not df.empty:
        response = {"joke": df["joke"][0], "joke_id": int(df["id"][0])}
    else:
        response = {"joke": "No more jokes to tag", "joke_id": -1}
    return response


@app.get("/jokes/validate/random")
async def get_random_validate_joke():
    """
    Returns a joke from the validate_jokes table, which has not been validated
    :return: json = {joke_id, joke}
    """
    df = validation.get_not_validated_joke()
    if not df.empty:
        response = {"joke": df["joke"][0], "joke_id": int(df["id"][0])}
    else:
        response = {"joke": "No more jokes to validate :D", "joke_id": -1}
    return response


@app.get("/notebooks/ratings")
async def get_ratings_notebook(request: Request):
    return templates.TemplateResponse("analysis_mail_users.html", {"request": request})
