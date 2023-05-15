from fastapi import Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse


class ExternalPostsApiException(HTTPException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=self.message)

class UnknownErrorException(Exception):
    def __init__(self, message: str):
        self.message = message

async def epa_exception_handler(request: Request, exc: ExternalPostsApiException):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"message": exc.message}
    )

async def uee_exception_handler(request: Request, exc: UnknownErrorException):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": "Internal Server Error!"}
    )