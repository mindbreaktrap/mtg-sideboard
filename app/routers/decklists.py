from fastapi import APIRouter, Request

from app.decklist_to_json import read_decklist
from app.models.decklists import Deck, Decklist
from app.models.responses import Created

router = APIRouter(prefix="/decklist", tags=["decklist"])


@router.post("/txt")
async def create_decklist_from_txt(request: Request):
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
    return await create_decklist_from_json(Deck(**decklist))  # type: ignore


@router.post(
    "/json",
    response_model=Created.Model,
    status_code=Created.status_code,
)
async def create_decklist_from_json(input: Deck):
    """This route takes a decklist in .json format and returns it."""
    result = Decklist(decklist=input)
    result = await result.insert()  # type: ignore
    return Created(str(result.id))
