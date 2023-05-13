from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

POSTS_TABLE = config.get("DATABASE", "posts_table")
USERS_TABLE = config.get("DATABASE", "users_table")


class User(Base):
    __tablename__ = USERS_TABLE
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)

    posts = relationship("Post", back_populates="user")

class Post(Base):
    __tablename__ = POSTS_TABLE

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    body = Column(String)
    
    user = relationship("User", back_populates="posts")