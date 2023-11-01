from fastapi import status
from fastapi.responses import JSONResponse


class Created(JSONResponse):
    """This class is used to return a 201 status code with the id of the created object."""

    def __init__(self, id: str):
        super().__init__(status_code=status.HTTP_201_CREATED, content={"id": id})


class BadRequest(JSONResponse):
    """This class is used to return a 400 status code with the error message."""

    def __init__(self, message: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST, content={"message": message}
        )
