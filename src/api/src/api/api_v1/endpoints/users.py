from fastapi import Depends, APIRouter
from starlette.requests import Request
from starlette.templating import Jinja2Templates

try:
    import src.auth.core as auth
    import src.db.users as db_users
    import src.models as models
    import src.mail.core as mail
    from src.mail.secret import MAILGUN_USER, MAILGUN_PWD
except ModuleNotFoundError:
    import src.api.src.auth.core as auth
    import src.api.src.db.users as db_users
    import src.api.src.models as models
    import src.api.src.mail.core as mail
    from src.api.rc.mail.secret import MAILGUN_USER, MAILGUN_PWD


router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/users/me", tags=["users"])
async def read_users_me(current_user: auth.User = Depends(auth.get_current_user)):
    """
    Gets the current logged via OAuth user information (in the model users_admin)
    :param current_user: Contains the user name, email, hashed password, disabled and scope information
    :return: returns current User
    """
    return current_user


@router.post("/users/telegram/add", tags=["users"], status_code=201)
async def add_user(user: models.TelegramUser, current_user: auth.User = Depends(auth.get_current_user)):
    """
    Adds a telegram user (the start function does so). Does not have much sense here, just for testing.
    Admin rights are needed for this one in order to keep the DB clean
    :param current_user: User model
    :param user: TelegramUser model
    :return: returns the created user
    """
    db_users.add_user_telegram(user.user_id, user.first_name)
    return user


async def send_mail_subscribed_user(email: str):
    is_sent = mail.send_subscribed_mail(MAILGUN_USER, MAILGUN_PWD, email)
    return {"is_sent": is_sent}


@router.post("/users/mail/add", tags=["users"], status_code=201)
async def add_mail_user(mail_user: models.MailUser):
    db_users.add_user_mail(mail_user.email)

    # send mail to subbed user
    await send_mail_subscribed_user(mail_user.email)
    return mail_user


@router.post("/users/mail/unsubscribed", tags=["users"], status_code=201)
async def unsubscribe_from_mail(request: Request):
    """
    Removes user from the distribution mail list
    :param request: Request object
    :return: returns MailUser model
    """

    d_email = dict(await request.form())
    is_removed, msg = db_users.soft_delete_user_mail(d_email["email"])

    if is_removed:
        # return {"message": msg, "is_removed": is_removed}
        return templates.TemplateResponse("unsubscribed.html", {"request": request})
    else:
        return {"message": msg, "is_removed": is_removed}


@router.get("/users", tags=["users"])
async def get_all_users(current_user: auth.User = Depends(auth.get_current_user)):
    d_users = db_users.get_users_mail().to_dict(orient="index")
    return d_users
