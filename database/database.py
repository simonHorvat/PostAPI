from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

CONN_STRING = config.get("DATABASE", "connection_string")


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally: db.close()

engine = create_engine(CONN_STRING)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()
