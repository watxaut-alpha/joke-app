import logging

from fastapi import APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

try:
    import src.models as models
    import src.helpers as helpers
    import src.db.jokes as jokes
    from src.api.api_v1.params import API_V_STR
except ModuleNotFoundError:
    import src.api.src.models as models
    import src.api.src.helpers as helpers
    import src.api.src.db.jokes as jokes
    from src.api.src.api.api_v1.params import API_V_STR

router = APIRouter()
templates = Jinja2Templates(directory="templates")
logger = logging.getLogger("jokeapp")


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
        b_rating = jokes.upsert_rating_joke(**user_rating.dict())
        if b_rating:
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


@router.get("/users/mail/subscribe", status_code=200, include_in_schema=False)
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
    is_sent = await helpers.put_user_db(d_email["email"])
    if is_sent:
        return templates.TemplateResponse("subscribed.html", {"request": request})
    else:
        return templates.TemplateResponse(
            "error.html",
            {
                "request": request,
                "status_code": 400,
                "err_txt": "Email does not have a correct syntax, get in touch with watxaut@gmail.com",
            },
        )


@router.get("/users/mail/unsubscribe", status_code=200, include_in_schema=False)
async def show_unsubscribe_page(request: Request):
    return templates.TemplateResponse("unsubscribe.html", {"request": request, "API_V_STR": API_V_STR})


@router.get("/notebooks/ratings", include_in_schema=False)
async def get_ratings_notebook(request: Request):
    return templates.TemplateResponse("exports/analysis_mail_users.html", {"request": request})
