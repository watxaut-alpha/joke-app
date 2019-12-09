import requests
from fastapi import APIRouter
from fastapi import Depends, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.templating import Jinja2Templates

try:
    import src.models as models
    import src.helpers as helpers
    from src.api.api_v1.params import API_V1_STR, TITLE, DESCRIPTION
    from src.db.secret import HOST
    from src.auth.secret import DOCS_USER, DOCS_PASSWORD
except ModuleNotFoundError:
    import src.api.src.models as models
    import src.api.src.helpers as helpers
    from src.api.src.api.api_v1.params import API_V1_STR
    from src.api.src.db.secret import HOST
    from src.api.src.auth.secret import DOCS_USER, DOCS_PASSWORD

router = APIRouter()
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()  # this one is only for /docs endpoint


@router.get("/", include_in_schema=False)
async def main(request: Request):
    """
    Main endpoint with no use at all, does not do very much. Shows an image of a cat using a free API.
    :param request: User GET Request
    :return: html with template index.html
    """
    url = helpers.get_cat_url()
    return templates.TemplateResponse("index.html", {"request": request, "url": url})


@router.get("/legal", include_in_schema=False)
async def legal(request: Request):
    """
    Shows the legal.html template with the legal agreement (for watxaut)
    :param request: User's GET Request
    :return: template with the html response
    """
    return templates.TemplateResponse("legal.html", {"request": request})


@router.get("/openapi.json", include_in_schema=False)
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
    return JSONResponse(get_openapi(title=TITLE, version=API_V1_STR, description=DESCRIPTION, routes=router.routes))


@router.get("/docs", include_in_schema=False)
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
    return get_swagger_ui_html(openapi_url="/openapi.json", title="{} Docs".format(TITLE))


@router.get("/jokes/rating/{joke_id}/{id_hash}/{rating}", include_in_schema=False)
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
        user_rating = models.UserRating(user_id=id_hash, joke_id=joke_id, rating=rating, source="mail")

        req = requests.put(f"{HOST}/{API_V1_STR}/jokes/rating", data=user_rating)
        if req:
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


@router.get("/users/mail/subscribe", status_code=200)
async def show_subscribe_page(request: Request):
    return templates.TemplateResponse("subscribe.html", {"request": request})


@router.post("/users/mail/subscribed", status_code=200, include_in_schema=False)
async def subscribe_user(request: Request):
    """
    Adds a user to the users_mail table. Every 8.30 (Spain Local Timezone) a cron sends a mail to every entry in the
    users_mail with a joke and the ability to rate it from the mail.
    :param request: Request object
    :return: returns a template
    """
    d_email = dict(await request.form())
    mail_user = models.MailUser(email=d_email["email"])
    req = requests.post(f"{HOST}/{API_V1_STR}/users/mail/add", data=mail_user)
    if req:
        return templates.TemplateResponse("subscribed.html", {"request": request})
    else:
        return templates.TemplateResponse(
            "error.html", {"request": request, "status_code": req.status_code, "err_txt": req.text}
        )


@router.get("/users/mail/unsubscribe", status_code=200)
async def show_unsubscribe_page(request: Request):
    return templates.TemplateResponse("unsubscribe.html", {"request": request})


@router.get("/notebooks/ratings")
async def get_ratings_notebook(request: Request):
    return templates.TemplateResponse("exports/analysis_mail_users.html", {"request": request})
