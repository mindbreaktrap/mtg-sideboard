from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field


class Created(JSONResponse):
    """This class is used to return a 201 status code with the id of the created object."""

    status_code: int = status.HTTP_201_CREATED

    def __init__(self, id: str):
        super().__init__(status_code=status.HTTP_201_CREATED, content={"id": id})


class BadRequest(JSONResponse):
    """This class is used to return a 400 status code with the error message."""

    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": message}
        )


class NotFound(JSONResponse):
    """This class is used to return a 404 status code with the error message."""

    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND, content={"message": message}
        )


class NotFoundResponseModel(BaseModel):
    message: str = Field(
        ...,
        description="The error message.",
        examples=[
            "Search for parameters deckname=Death's Shadow and id=b85e8501-b827-41a8-8ba9-1dcb99860be8 returned no results."
        ],
    )


class BadRequestResponseModel(BaseModel):
    message: str = Field(
        ...,
        description="The error message.",
        examples=["badly formed hexadecimal UUID string"],
    )


class CreatedResponseModel(BaseModel):
    id: str = Field(
        ...,
        description="The id of the created object.",
        examples=["b85e8501-b827-41a8-8ba9-1dcb99860be8"],
    )
