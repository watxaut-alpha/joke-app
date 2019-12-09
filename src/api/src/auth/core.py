import datetime
from datetime import timedelta

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError
from pydantic import BaseModel
from starlette.status import HTTP_401_UNAUTHORIZED

try:
    import src.db.users as users
    from src.auth.secret import ALGORITHM, SECRET_KEY
except ModuleNotFoundError:
    import src.api.src.db.users as users
    from src.api.src.auth.secret import ALGORITHM, SECRET_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")


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


def get_user(username: str) -> [UserInDB, None]:
    df = users.get_admin_users()
    if username in df["username"].values:
        print(username)
        df = df[df["username"] == username]
        user_dict = df.to_dict(orient="index")[0]
        return UserInDB(**user_dict)
    return None


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
        token_data = TokenData(username=username)
    except PyJWTError:
        raise credentials_exception
    user = get_user(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


# OAuth User login. Code gotten from https://fastapi.tiangolo.com/tutorial/security/intro/ and adapted for my app
async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def authenticate_user(pwd_context, username: str, password: str) -> [UserInDB, None]:
    user = get_user(username)
    if user is None:
        return None
    if not verify_password(pwd_context, password, user.hashed_password):
        return None
    return user


def create_access_token(*, data: dict, expires_delta: timedelta = None) -> bytes:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(pwd_context, password) -> str:
    return pwd_context.hash(password)


def verify_password(pwd_context, plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
