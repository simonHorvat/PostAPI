from fastapi import FastAPI
from .routes import posts
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

TITLE = config.get("APP", "title")
DESC = config.get("APP", "description")

app = FastAPI(title=TITLE,
              description=DESC)

app.include_router(posts.router)
#app.include_router(users.router)
