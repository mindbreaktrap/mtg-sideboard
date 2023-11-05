import uuid

from beanie import Document
from pydantic import BaseModel, Field, model_validator


class BoardingInput(BaseModel):
    deckname: str = Field(..., examples=["UB Shadow"])
    deck_id: uuid.UUID = Field(
        default=None,
        examples=[str(uuid.uuid4())],
        description="ID of the deck the boarding belongs to.",
    )
    """The endpoint will validate that this exists."""
    opponent: str = Field(..., examples=["Jeskai Control"])
    on_the_play: bool = Field(True, examples=[True, False])
    cards_coming_in: dict = Field(
        ...,
        examples=[
            {
                "Brazen Borrower": 1,
                "Dauthi Voidwalker": 1,
                "Dress Down": 1,
            }
        ],
    )
    cards_going_out: dict = Field(
        ...,
        examples=[
            {
                "Thoughtseize": 2,
                "Force of Will": 1,
            }
        ],
    )

    # validate that we are not boarding out more than we are boarding in
    @model_validator(mode="after")
    def validate_boarding(self) -> "BoardingInput":
        cards_coming_in = sum(self.cards_coming_in.values())
        if cards_coming_in == 0:
            raise ValueError("You must board in at least one card.")
        if cards_coming_in > 15:
            raise ValueError("You cannot board in more than 15 cards.")
        cards_going_out = sum(self.cards_going_out.values())
        if cards_going_out > 15:
            raise ValueError("You cannot board out more than 15 cards.")
        if cards_coming_in < cards_going_out:
            raise ValueError(
                "You are boarding out more cards than you are boarding in."
            )
        return self


class Boarding(BoardingInput, Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")

    class Settings:
        name = "boardings"
