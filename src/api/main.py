from fastapi import FastAPI
from starlette.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

try:
    import src.api.api_v1.api as api_v1
    import src.frontend.endpoints as frontend
    from src.api.api_v1.params import API_V1_STR, TITLE, DESCRIPTION
except ModuleNotFoundError:
    import src.api.src.api.api_v1.api as api_v1
    import src.api.src.frontend.endpoints as frontend
    from src.api.src.api.api_v1.params import API_V1_STR, TITLE, DESCRIPTION

# prod
# uvicorn main:app --host 0.0.0.0 --port 80
# Test
# uvicorn main:app --reload


# Create FastApi app (has to be named like this)
app = FastAPI(title=TITLE, description=DESCRIPTION, docs_url=None, redoc_url=None, openapi_url=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.exception_handler(404)
async def not_found(request, exc):
    return templates.TemplateResponse("fpqll.html", {"request": request}, status_code=404)


app.include_router(frontend.router)
app.include_router(api_v1.api_router, prefix=API_V1_STR)
