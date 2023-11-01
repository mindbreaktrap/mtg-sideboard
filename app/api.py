import json
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.db import init
from app.decklist_to_json import read_decklist
from app.models.decklist import Deck, Decklist


@asynccontextmanager
async def lifespan(api: FastAPI):
    await init()
    yield


api = FastAPI(lifespan=lifespan)


# exception handler for pydantic validation errors
@api.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


@api.post("/decklist/txt")
async def decklist_txt_to_json(request: Request):
    """This route takes a decklist in .txt format and converts it to json.\n
    Example:\n
    4 Entomb\n
    4 Faithless Looting\n
    4 Reanimate\n
    \n
    SIDEBOARD:\n
    2 Wear//Tear\n
    """
    decklist = await request.body()
    decklist = read_decklist(decklist.decode("utf-8")).get("decklist")
    try:
        return await decklist_json_to_database(Deck(**decklist))  # type: ignore
    except ValueError:
        return JSONResponse(
            status_code=400, content={"message": "Invalid decklist format."}
        )


@api.post("/decklist/json")
async def decklist_json_to_database(input: Deck):
    """This route takes a decklist in .json format and returns it."""
    result = Decklist(decklist=input)
    result = await result.insert()  # type: ignore
    return JSONResponse(
        status_code=status.HTTP_201_CREATED, content={"id": str(result.id)}
    )
