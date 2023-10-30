import json
from datetime import datetime


def input_metadata() -> dict:
    """Asks the user for the deck title and author name and returns a dict with the metadata."""
    # get decktitle from user input
    decktitle = input("Enter the deck title: ")
    # get author name from user input
    author = input("Enter the author name: ")
    # calculate date in form Month Day, Year
    date = datetime.today().strftime("%B %d, %Y")
    return {"title": decktitle, "author": author, "date": date}


def read_decklist(path: str) -> dict:
    """Reads a decklist from a txt file and returns a dict with the decklist separated into MB and SB."""
    # create a list of all lines from the input path txt
    # remove newlines and empty lines
    with open(path, "r") as f:
        lines = f.readlines()
        lines = [line.strip() for line in lines]
        lines = list(filter(None, lines))

    # split the list at occurence of word "SIDEBOARD" into two parts
    # first part is the mainboard, second part is the sideboard
    mainboard = lines[: lines.index("SIDEBOARD:")]
    sideboard = lines[lines.index("SIDEBOARD:") + 1 :]

    # create a list of all cards in the mainboard
    # the cardname is the key and the amount is the value
    mainboard_cards = {}
    for card in mainboard:
        cardname = card[card.index(" ") + 1 :]
        amount = int(card[: card.index(" ")])
        mainboard_cards[cardname] = amount

    # do the same for sideboard cards
    sideboard_cards = {}
    for card in sideboard:
        cardname = card[card.index(" ") + 1 :]
        amount = int(card[: card.index(" ")])
        sideboard_cards[cardname] = amount

    return {"decklist": {"maindeck": mainboard_cards, "sideboard": sideboard_cards}}


if __name__ == "__main__":
    metadata = input_metadata()
    decklist = read_decklist("shadow.txt")
    # merge those dicts
    decklist.update(metadata)

    # TODO ask for screen names
    decklist.update({"screen_names": {}})

    # TODO get matchups
    decklist.update({"matchups": {}})

    # save json to file
    with open("shadow.json", "w") as f:
        json.dump(decklist, f, indent=4)
