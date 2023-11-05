import uuid
from typing import Dict

from beanie import Document
from pydantic import BaseModel, Field, field_validator


class DecklistInput(BaseModel):
    deckname: str = Field(..., examples=["UB Shadow"])
    maindeck: Dict[str, int] = Field(
        ...,
        examples=[
            {
                "Brainstorm": 4,
                "Dauthi Voidwalker": 1,
                "Daze": 4,
                "Death's Shadow": 4,
                "Dismember": 1,
                "Dress Down": 1,
                "Flooded Strand": 1,
                "Force of Will": 4,
                "Island": 1,
                "Murktide Regent": 3,
                "Orcish Bowmasters": 4,
                "Polluted Delta": 4,
                "Ponder": 4,
                "Reanimate": 3,
                "Snuff Out": 1,
                "Street Wraith": 3,
                "Swamp": 1,
                "Thoughtseize": 4,
                "Troll of Khazad-d\u00fbm": 3,
                "Underground Sea": 2,
                "Wasteland": 4,
                "Watery Grave": 3,
            }
        ],
    )
    sideboard: Dict[str, int] = Field(
        ...,
        examples=[
            {
                "Brazen Borrower": 1,
                "Dauthi Voidwalker": 1,
                "Dress Down": 1,
                "Fatal Push": 2,
                "Force of Negation": 2,
                "Hydroblast": 1,
                "Null Rod": 1,
                "Palant\u00edr of Orthanc": 1,
                "Plague Engineer": 1,
                "Powder Keg": 1,
                "Sheoldred's Edict": 1,
                "Surgical Extraction": 2,
            }
        ],
    )
    screen_names: Dict[str, str] = Field(
        ...,
        examples=[
            {
                "Brazen Borrower": "BB",
                "Dauthi Voidwalker": "Dauthi",
                "Fatal Push": "Push",
            }
        ],
    )

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


class Decklist(DecklistInput, Document):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, alias="_id")

    class Settings:
        name = "decklists"
