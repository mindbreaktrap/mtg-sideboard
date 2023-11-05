import uuid

from fastapi import APIRouter, status

from app.models.boardings import Boarding, BoardingInput
from app.models.decklists import Decklist
from app.models.responses import (
    BadRequest,
    Created,
    CreatedResponseModel,
    NotFound,
    NotFoundResponseModel,
)

router = APIRouter(prefix="/boardings", tags=["Boardings"])


@router.post(
    "",
    response_model=CreatedResponseModel,
    status_code=Created.status_code,
)
async def create_boarding_for_matchup(input: BoardingInput):
    """This route takes a boarding in .json format and inserts it into the db."""
    if await Decklist.get(input.deck_id) is None:
        raise ValueError(f"Deck with id {input.deck_id} does not exist.")
    result = Boarding(**input.model_dump())
    result = await result.insert()  # type: ignore
    return Created(str(result.id))


@router.get(
    "",
    response_model=list[Boarding],
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {"model": NotFoundResponseModel},
    },
)
async def get_boarding(deckname: str | None = None, id: uuid.UUID | None = None):
    """This route returns a list of boardings from the db by deckname and/or id."""
    # CASE 1: no parameters are given, return all boardings
    if deckname is None and id is None:
        results = Boarding.find_many({})
        if results is None:
            return NotFound("There are no boardings in the database.")
        return [result async for result in results]

    # CASE 2: we have both a deckname and an id, so we can do a direct lookup and make sure the deckname matches
    elif deckname is not None and id is not None:
        result = await Boarding.get(id)
        if result is None:
            return NotFound(f"Decklist with id {id} does not exist.")
        if result.deckname != deckname:
            return BadRequest(
                f"Decklist with id {id} does not match given deckname {deckname}."
            )
        return [result]

    # CASE 3: we have an ID and can do a direct lookup
    elif id is not None:
        result = await Boarding.get(id)
        if result is None:
            return NotFound(f"Decklist with id {id} does not exist.")
        return [result]

    # CASE 4: we have a deckname and need to do a lookup for potentially multiple boardings
    elif deckname is not None:
        results = Boarding.find_many({"deckname": deckname})
        if results is None:
            return NotFound(f"There are no boardings for decklist {deckname}.")
        return [result async for result in results]
