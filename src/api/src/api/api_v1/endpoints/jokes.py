from fastapi import APIRouter, Depends
from starlette.templating import Jinja2Templates

try:
    import src.auth.core as auth
    import src.db.jokes as jokes
    import src.db.validation as validation
    import src.models as models
except ModuleNotFoundError:
    import src.api.src.auth.core as auth
    import src.api.src.db.jokes as jokes
    import src.api.src.db.validation as validation
    import src.api.src.models as models

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/jokes/random", tags=["jokes"])
async def send_random_joke():
    """
    Gets a random joke from the jokes table (already validated)
    :return: json response = {joke_id, joke}
    """
    df = jokes.get_random_joke()
    response = {"joke_id": int(df["id"][0]), "joke": df["joke"][0]}
    return response


# define the same method but with put
@router.put("/jokes/rating", tags=["jokes"])
async def joke_rating_put(user_rating: models.UserRating):
    """
    The same method as above, but with put so much more secure
    :param user_rating: UserRating Model
    :return: returns json with success or fail
    """

    b_rating = jokes.upsert_rating_joke(**user_rating.dict())
    if b_rating:
        return {"message": "success"}
    else:
        return {"message": "Error"}


@router.get("/jokes/next", tags=["jokes"])
async def get_5_next_jokes(current_user: auth.User = Depends(auth.get_current_user)):
    df = jokes.get_5_next_jokes_to_send().drop(["do_send", "rating", "tags", "created_at"], axis=1)
    s = df.to_dict(orient="index")
    return s


@router.put("/jokes/validate", tags=["jokes"])
async def update_joke_validation(user_validation: models.UserValidation):
    """
    Jokes coming from scraped websites must be validated before going to jokes table, this function updates
    the validate_jokes table
    :param user_validation: UserValidation Model
    :return: json
    """
    validation.update_joke_validation(**user_validation.dict())
    return {"message": "success"}


@router.get("/jokes/tags", tags=["jokes"])
async def get_tags():
    """
    Gets available tags for jokes from tags table
    :return: json = {tags: l_tags}
    """
    l_tags = jokes.get_tags()
    return {"tags": l_tags}


@router.post("/jokes/add", tags=["jokes"])
async def add_joke(user_joke: models.UserJoke, current_user: auth.User = Depends(auth.get_current_user)):
    jokes.put_joke_db(**user_joke.dict())
    return {"message": "success"}


@router.put("/jokes/tag", tags=["jokes"])
async def tag_joke(user_tag: models.UserTag):
    """
    Tags a joke from jokes table
    :param user_tag: UserTag Model
    :return: json
    """
    jokes.upsert_joke_tag(**user_tag.dict())
    return {"message": "success"}


@router.get("/jokes/tags/random", tags=["jokes"])
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


@router.get("/jokes/validate/random", tags=["jokes"])
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
