from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.db import init
from app.decklist_to_json import read_decklist
from app.models.decklist import Deck, Decklist
from app.models.responses import BadRequest, Created


@asynccontextmanager
async def lifespan(api: FastAPI):
    await init()
    yield


api = FastAPI(lifespan=lifespan)


# exception handler for pydantic value errors
@api.exception_handler(ValueError)
async def validation_exception_handler(request: Request, exc: ValueError):
    return BadRequest(str(exc))


@api.post("/decklist/txt")
async def decklist_txt_to_json(request: Request):
    """This route takes a decklist in .txt format and converts it to json.\n

    Note: This adheres to the model in /decklist/json so make sure the decklist is valid.\n

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
    return await decklist_json_to_database(Deck(**decklist))  # type: ignore


@api.post(
    "/decklist/json",
    response_model=Created.Model,
    status_code=Created.status_code,
)
async def decklist_json_to_database(input: Deck):
    """This route takes a decklist in .json format and returns it."""
    result = Decklist(decklist=input)
    result = await result.insert()  # type: ignore
    return Created(str(result.id))
