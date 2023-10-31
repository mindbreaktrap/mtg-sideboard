from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.db import init
from app.decklist_to_json import read_decklist
from app.models import Decklist


@asynccontextmanager
async def lifespan(api: FastAPI):
    await init()
    yield


api = FastAPI(lifespan=lifespan)


@api.post("/decklist/txt")
async def decklist_txt_to_json(request: Request):
    """This route takes a decklist in .txt format and converts it to json."""
    decklist = await request.body()
    # convert binary to string
    decklist = decklist.decode("utf-8")
    # save decklist to temporary file with random name
    try:
        return read_decklist(decklist)
    except ValueError:
        return JSONResponse(
            status_code=400, content={"message": "Invalid decklist format."}
        )


@api.post("/decklist/json")
async def decklist_json_to_json(input: Decklist):
    """This route takes a decklist in .json format and returns it."""
    await Decklist.insert_one(input)
    return None
