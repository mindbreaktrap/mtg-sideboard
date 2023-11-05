import uuid
from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field, model_validator


class BoardingInput(BaseModel):
    deckname: str = Field(..., examples=["Death's Shadow"])
    deck_id: Optional[uuid.UUID] = Field(default=None, examples=[str(uuid.uuid4())])
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
        cards_coming_in = self.cards_coming_in
        cards_going_out = self.cards_going_out
        if sum(cards_coming_in.values()) < sum(cards_going_out.values()):
            raise ValueError(
                "You are boarding out more cards than you are boarding in."
            )
        return self


class Boarding(BoardingInput, Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")

    class Settings:
        name = "boardings"
