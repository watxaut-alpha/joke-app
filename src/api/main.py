from fastapi import Depends, HTTPException
from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette.responses import JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.status import HTTP_401_UNAUTHORIZED
from starlette.templating import Jinja2Templates

try:
    import src.api.api_v1.api as api_v1
    import src.frontend.endpoints as frontend
    from src.api.api_v1.params import API_V1_STR, TITLE, DESCRIPTION
    from src.auth.secret import DOCS_USER, DOCS_PASSWORD
except ModuleNotFoundError:
    import src.api.src.api.api_v1.api as api_v1
    import src.api.src.frontend.endpoints as frontend
    from src.api.src.api.api_v1.params import API_V1_STR, TITLE, DESCRIPTION
    from src.api.src.auth.secret import DOCS_USER, DOCS_PASSWORD

# prod
# uvicorn main:app --host 0.0.0.0 --port 80
# Test
# uvicorn main:app --reload


# Create FastApi app (has to be named like this)
app = FastAPI(title=TITLE, description=DESCRIPTION, docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
security = HTTPBasic()  # this one is only for /docs endpoint


@app.exception_handler(404)
async def not_found(request, exc):
    return templates.TemplateResponse("fpqll.html", {"request": request}, status_code=404)


app.include_router(frontend.router)
app.include_router(api_v1.api_router, prefix=API_V1_STR)


@app.get(f"{API_V1_STR}/openapi.json", include_in_schema=False)
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
    return JSONResponse(get_openapi(title=TITLE, version=API_V1_STR, description=DESCRIPTION, routes=app.routes))


@app.get(f"{API_V1_STR}/docs", include_in_schema=False)
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
    return get_swagger_ui_html(openapi_url=f"{API_V1_STR}/openapi.json", title="{} Docs".format(TITLE))
