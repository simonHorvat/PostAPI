from pydantic import BaseModel

class InfoMessage(BaseModel):
    message: str
