import uuid
from typing import Dict

from beanie import Document
from pydantic import BaseModel, Field, field_validator


class Deck(BaseModel):
    maindeck: Dict[str, int] = Field(
        ..., examples=[{"Entomb": 4, "Faithless Looting": 4}]
    )
    sideboard: Dict[str, int] = Field(..., examples=[{"Wear//Tear": 2}])

    @field_validator("maindeck")
    def validate_maindeck(cls, maindeck):
        if sum(maindeck.values()) < 60:
            raise ValueError("Illegal maindeck size. Should be at least 60 cards.")
        return maindeck

    @field_validator("sideboard")
    def validate_sideboard(cls, maindeck):
        if sum(maindeck.values()) != 15:
            raise ValueError("Illegal sideboard size. Should be 15 cards.")
        return maindeck


class Decklist(Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")
    decklist: Deck

    class Settings:
        name = "decklists"


if __name__ == "__main__":
    # Test with too small deck
    try:
        deck = Deck(maindeck={"Forest": 20}, sideboard={"Giant Growth": 15})
    except ValueError:
        print("Deck validation failed as expected.")
    else:
        raise AssertionError("Deck validation should have failed.")

    # Test with valid deck
    try:
        deck = Deck(maindeck={"Forest": 60}, sideboard={"Giant Growth": 15})
        print("Deck validation passed as expected.")
    except ValueError:
        raise AssertionError("Deck validation should have passed.")

    # Test with no sideboard
    try:
        deck = Deck(maindeck={"Forest": 60}, sideboard={})
    except ValueError:
        print("Deck validation failed as expected.")

    # Test with completely empty deck
    try:
        deck = Deck(maindeck={}, sideboard={})
    except ValueError:
        print("Deck validation failed as expected.")
    else:
        raise AssertionError("Deck validation should have failed.")