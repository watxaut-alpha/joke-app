from datetime import timedelta

from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED

import src.api.auth as auth

router = APIRouter()

# Creates a encryption context with Bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ACCESS_TOKEN_EXPIRE_MINUTES = 30


class Token(BaseModel):
    access_token: str
    token_type: str


# OAuth User login. Code gotten from https://fastapi.tiangolo.com/tutorial/security/intro/ and adapted for my app
@router.post("/token", response_model=Token, tags=["login"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(pwd_context, form_data.username, form_data.password)
    if user is None:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/login/test-token", tags=["login"], response_model=auth.User)
def test_token(current_user: auth.User = Depends(auth.get_current_user)):
    """
    Test access token
    """
    return current_user
