from .models import User, Post
from .database import Base, engine, SessionLocal
import logging
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

LOG_FORMAT = config.get("LOGGING", "format")

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
formatter = logging.Formatter(LOG_FORMAT)
ch.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(ch)

def load_toy_data():
    Base.metadata.create_all(bind=engine)  # create tables if they don't exist
    db = SessionLocal()  # get a database session
    try:
        # check if User and Post tables are empty
        if db.query(User).count() == 0 and db.query(Post).count() == 0:
            # create some users
            users = [
                User(name="Alice", email="alice@example.com", phone="123-456-7890"),
                User(name="Bob", email="bob@example.com", phone="555-555-5555"),
                User(name="Charlie", email="charlie@example.com", phone="999-999-9999"),
            ]
            db.add_all(users)  # add users to the database

            # create some posts
            posts = [
                Post(userId=1, title="My first post", body="Hello, world!"),
                Post(userId=2, title="My second post", body="This is a post."),
                Post(userId=3, title="Another post", body="This is another post."),
            ]
            db.add_all(posts)  # add posts to the database
            db.commit()  # save changes to the database
            logger.info("Data loaded successfully!")
        else:
            logger.info("Database already has data.")
        
    except Exception as error:
        db.rollback()  # undo changes if an error occurred
        logger.error(f"Error loading data. --> {error}")
    finally:
        db.close()  # close the database session

load_toy_data()
