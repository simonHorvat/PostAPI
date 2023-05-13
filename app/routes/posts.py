from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import requests
import logging

from database.database import get_db
from database.models import Post as PostModel
from schemas.post_schema import Post as PostSchema
from schemas.info_message_schema import InfoMessage
from app.utils import valid_id
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

LOG_FORMAT = config.get("LOGGING", "format")
GET_POST_DESC = config.get("ROUTES", "get_post")
GET_POSTS_DESC = config.get("ROUTES", "get_posts")
CREATE_POST_DESC = config.get("ROUTES", "create_post")
EDIT_POST_DESC = config.get("ROUTES", "edit_post")
DELETE_POST_DESC = config.get("ROUTES", "delete_post")
API_POSTS_URL = config.get("EXTERNAL_API", "posts_url")
API_USERS_URL = config.get("EXTERNAL_API", "users_url")


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(LOG_FORMAT)
ch.setFormatter(formatter)
logger.addHandler(ch)

router = APIRouter()


@router.get("/post/{id}", description=GET_POST_DESC)
async def get_post(id: int, db: Session = Depends(get_db)) -> PostSchema:
    logger.info(f"GET request received for post id: {id}")
    try:
        # Check that the post ID is valid
        if not valid_id(id):
            raise HTTPException(status_code=400, detail=f"Invalid post id={id}, id must be positive integer")
        
        # Attempt to retrieve the post from the database
        post = db.query(PostModel).filter(PostModel.id == id).first()
        if post: # If the post is found in the database, return it as a PostSchema object
            return PostSchema.from_orm(post)

        # If the post is not found in the database, retrieve it from an external API
        url = f"{API_POSTS_URL}/{id}"
        with requests.get(url) as response:
            if response.status_code != 200: 
                raise HTTPException(status_code=404, detail=f"The request to the external API failed with error, check if a post with the given id exists")
            
            content = response.json()
            new_post = PostModel(id=content['id'], userId=content['userId'], title=content['title'], body=content['body'])
            post_schema = PostSchema.from_orm(new_post)
            db.add(new_post)
            db.commit()
            return post_schema
            
    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.exception(f"An error occurred while processing get request for post id: {id}")
        raise e


@router.get("/posts/{userId}", description=GET_POSTS_DESC)
async def get_posts(userId: int, db: Session = Depends(get_db)) -> List[PostSchema]:
    
    # Log the fact that a GET request has been received for a particular user
    logger.info(f"GET request received for user id: {userId}")
    
    try:
        # Check if the user id is valid
        if not valid_id(userId):
            raise HTTPException(status_code=404, detail=f"Invalid userId={userId}, id must be positive integer")
        
        # Query the database for all posts belonging to the user with the given id
        posts = db.query(PostModel).filter(PostModel.userId == userId).all()
        # Convert the queried posts into a list of PostSchemas
        return [PostSchema.from_orm(post) for post in posts]
    
    except HTTPException as e:
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.exception(f"An error occurred while processing request for post id: {id}")
        raise e


@router.post("/create", description=CREATE_POST_DESC)
async def create(post: PostSchema, db: Session = Depends(get_db)) -> PostSchema:
    # log the incoming request
    logger.info(f"POST request received to create a new post: {post}")
    try:
        # check if user with the given userId exists, raise an exception if user doesn't exist
        url = f"{API_USERS_URL}/{post.userId}"
        with requests.get(url) as response:
            if response.status_code != 200:
                raise HTTPException(status_code=400, detail=f"User with id={post.userId} not found")

        # create a new post and save it to the database
        new_post = PostModel(userId=post.userId, title=post.title, body=post.body)
        db.add(new_post)
        db.commit()
        return PostSchema.from_orm(new_post)

    except HTTPException as e:
        db.rollback()
        logger.error(str(e))
        raise e
    except Exception as e:
        logger.exception(f"An error occurred while processing request to create a new post: {str(e)}")
        db.rollback()
        raise e


@router.delete("/remove/{id}", description=DELETE_POST_DESC)
async def delete(id: int, db: Session = Depends(get_db)) -> InfoMessage:
    try:
        # Check if the id is a positive integer
        if not valid_id(id):
            raise HTTPException(status_code=404, detail=f"Invalid post id={id}, id must be positive integer")
        
        # Query the database for the post with the given id
        post = db.query(PostModel).filter(PostModel.id == id).first()
        
        # If the post doesn't exist, raise an HTTPException
        if post is None:
            raise HTTPException(status_code=404, detail=f"Post with id={id} not found")
        
        # If the post exists, delete it from the database and commit the changes
        db.delete(post)
        db.commit()
        
        # Log the deletion and return an InfoMessage indicating the post was deleted
        logger.info(f"Post with id={id} deleted")
        return InfoMessage(message=f"Post with id={id} deleted")
    
    except HTTPException as e:
        db.rollback()
        logger.error(str(e))
        raise e
    except Exception as e: 
        db.rollback()
        logger.exception(f"An error occurred while processing request to delete a post: {str(e)}")
        raise e


@router.put("/edit/{id}", description=EDIT_POST_DESC)
async def edit(id: int, title: Optional[str] = None, body: Optional[str] = None, db: Session = Depends(get_db)) -> PostSchema:
    try: 
        # Check if the post id is a valid positive integer
        if not valid_id(id):
            raise HTTPException(status_code=404, detail=f"Invalid post id={id}, id must be positive integer")
        
        # Get the post from the database based on the id
        post = db.query(PostModel).filter(PostModel.id == id).first()
        
        # If the post is not found, raise an HTTP exception
        if post is None:
            logger.error(f"Post with id={id} not found")
            raise HTTPException(status_code=404, detail=f"Post with id={id} not found")

        # If the 'title'/'body parameter is not None, update the post's 'title'/'body and log the update
        if title is not None: 
            post.title = title
            logger.info(f"Post title updated: {id}")
        
        if body is not None: 
            post.body = body
            logger.info(f"Post body updated: {id}")

        # Convert the updated post to a PostSchema object, commit the changes to the database and return edited post
        db.commit()
        logger.info(f"Post updated: {id}")
        
        return PostSchema.from_orm(post)
    
    except HTTPException as e:
        db.rollback()
        logger.error(str(e))
        raise e    
    except Exception as e:
        db.rollback()
        logger.exception(f"An error occurred while processing request to edit a post: {str(e)}")
        raise e
