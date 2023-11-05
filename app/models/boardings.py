import uuid
from typing import Optional

from beanie import Document
from pydantic import BaseModel, Field, model_validator


class BoardingInput(BaseModel):
    deckname: str = Field(..., examples=["Death's Shadow"])
    deck_id: Optional[uuid.UUID] = Field(
        default=None,
        examples=[str(uuid.uuid4())],
        description="Optional ID of the deck the boarding belongs to.",
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


if __name__ == "__main__":
    # Test with too many cards going out
    try:
        boarding = BoardingInput(
            deckname="Death's Shadow",
            opponent="Jeskai Control",
            on_the_play=True,
            cards_coming_in={"Brazen Borrower": 1, "Dauthi Voidwalker": 1},
            cards_going_out={"Thoughtseize": 2, "Force of Will": 1},
        )
    except ValueError:
        print("Boarding validation failed as expected.")
    else:
        raise AssertionError("Boarding validation should have failed.")

    # Test with valid boarding
    try:
        boarding = BoardingInput(
            deckname="Death's Shadow",
            opponent="Jeskai Control",
            on_the_play=True,
            cards_coming_in={
                "Brazen Borrower": 1,
                "Dauthi Voidwalker": 1,
                "Dress Down": 1,
            },
            cards_going_out={"Thoughtseize": 2, "Force of Will": 1},
        )
        print("Boarding validation passed as expected.")
    except ValueError:
        raise AssertionError("Boarding validation should have passed.")

    # Test with 16 cards going in
    try:
        boarding = BoardingInput(
            deckname="Death's Shadow",
            opponent="Jeskai Control",
            on_the_play=True,
            cards_coming_in={
                "Brazen Borrower": 4,
                "Dauthi Voidwalker": 4,
                "Dress Down": 4,
                "Fatal Push": 4,
            },
            cards_going_out={"Thoughtseize": 2, "Force of Will": 1},
        )
    except ValueError:
        print("Boarding validation failed as expected.")
    else:
        raise AssertionError("Boarding validation should have failed.")

    # Test with 16 cards going out
    try:
        boarding = BoardingInput(
            deckname="Death's Shadow",
            opponent="Jeskai Control",
            on_the_play=True,
            cards_coming_in={
                "Brazen Borrower": 1,
                "Dauthi Voidwalker": 1,
                "Dress Down": 1,
            },
            cards_going_out={
                "Thoughtseize": 4,
                "Force of Will": 4,
                "Fatal Push": 4,
                "Drown in the Loch": 4,
            },
        )
    except ValueError:
        print("Boarding validation failed as expected.")
    else:
        raise AssertionError("Boarding validation should have failed.")

    # Test with empty boarding
    try:
        boarding = BoardingInput(
            deckname="Death's Shadow",
            opponent="Jeskai Control",
            on_the_play=True,
            cards_coming_in={},
            cards_going_out={},
        )
    except ValueError:
        print("Boarding validation failed as expected.")
    else:
        raise AssertionError("Boarding validation should have failed.")

    # Test with cards going in but no cards coming out
    try:
        boarding = BoardingInput(
            deckname="Death's Shadow",
            opponent="Jeskai Control",
            on_the_play=True,
            cards_coming_in={
                "Brazen Borrower": 1,
                "Dauthi Voidwalker": 1,
                "Dress Down": 1,
            },
            cards_going_out={},
        )
        print("Boarding validation passed as expected.")
    except ValueError:
        raise AssertionError("Boarding validation should have passed.")
