from fastapi import HTTPException
from pydantic import BaseModel, validator
from typing import Optional
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

AT_LEAST_N_LETT = int(config.get("VALIDATION", "at_least_n_letters"))
AT_LEAST_N_WORDS = int(config.get("VALIDATION", "at_least_n_words"))

class Post(BaseModel):
    id: Optional[int]
    userId: int
    title: str
    body: str

    @validator("id")
    @validator("userId", allow_reuse=True)
    def non_negative_int(cls, id: Optional[int]):
        if id is None or (isinstance(id, int) and id>0): return id
        else: raise HTTPException(status_code=400, detail='id/userId must be positive integer')   

    @validator("title")
    def at_least_n_words(cls, title: str):
        if isinstance(title, str) and ' ' in title and len(title.split(" ")) >= AT_LEAST_N_WORDS: return title
        else: raise HTTPException(status_code=400, detail=f'title must contain at least {AT_LEAST_N_WORDS} words')    

    @validator("body")
    def at_least_n_letters(cls, body: str):
        if isinstance(body, str) and len(body) >= AT_LEAST_N_LETT: return body
        else: raise HTTPException(status_code=400, detail=f'body must contain at least {AT_LEAST_N_LETT} letters (whitespace characters included)')    

    class Config:
        orm_mode = True