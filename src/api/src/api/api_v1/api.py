from fastapi import APIRouter

import src.api.api_v1.endpoints.jokes as jokes
import src.api.api_v1.endpoints.login as login
import src.api.api_v1.endpoints.users as users

api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(jokes.router, tags=["jokes"])
api_router.include_router(users.router, tags=["users"])
