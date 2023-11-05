from fastapi import APIRouter

from app.models.boardings import Boarding, BoardingInput
from app.models.decklists import Decklist
from app.models.responses import Created

router = APIRouter(prefix="/boarding", tags=["boarding"])


@router.post("/", response_model=Created.Model, status_code=Created.status_code)
async def create_boarding_for_matchup(input: BoardingInput):
    """This route takes a boarding in .json format and inserts it into the db."""
    # if the deck_id is not None, make sure it exists in the db
    if input.deck_id is not None:
        deck = await Decklist.get(input.deck_id)
        if deck is None:
            raise ValueError("Deck with id {} does not exist.".format(input.deck_id))
    result = Boarding(**input.model_dump())
    result = await result.insert()  # type: ignore
    return Created(str(result.id))
