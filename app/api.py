from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.decklist_to_json import read_decklist
from app.convert_json_to_txt import table_header, boarding_in, boarding_out

app = FastAPI()


class Maindeck(BaseModel):
    """Consists of atleast 60 cards."""

    maindeck: dict[str, int]


class Sideboard(BaseModel):
    """Consists of exactly 15 cards."""

    sideboard: dict[str, int]


class Decklist(BaseModel):
    maindeck: Maindeck
    sideboard: Sideboard


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/decklist/txt")
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


@app.post("/decklist/json")
async def decklist_json_to_json(input: Decklist):
    """This route takes a decklist in .json format and returns it."""
    result = table_header()
    result += boarding_in(input.maindeck, input.sideboard)
