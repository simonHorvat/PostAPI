from fastapi import FastAPI
import configparser
from .routes import posts
from . import exceptions as exc


config = configparser.ConfigParser()
config.read("config.ini")

TITLE = config.get("APP", "title")
DESC = config.get("APP", "description")

app = FastAPI(title=TITLE,
              description=DESC)

app.add_exception_handler(exc.ExternalPostsApiException, exc.epa_exception_handler)
app.add_exception_handler(exc.UnknownErrorException, exc.uee_exception_handler)

app.include_router(posts.router)
#app.include_router(users.router)
