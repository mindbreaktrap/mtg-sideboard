"""
This script helps you create boarding guides for your deck.
It will ask for cards you are boarding in and out for each matchup.
The data will then be sent to the locally served backend and inserted into the DB for later usage.
"""


import json

import requests


def ask_for_screennames(decklist: dict) -> dict:
    all_cards = list(decklist["maindeck"].keys()) + list(decklist["sideboard"].keys())
    # sort them alphabetically
    all_cards.sort()
    # remove duplicates
    all_cards = list(dict.fromkeys(all_cards))
    # ask for screen names for all cards
    result = {}
    for card in all_cards:
        tmp = input(f"Enter screen name for {card}: ")
        if tmp != "":
            result[card] = tmp
    return result


def boarding(opp: str, decklist: dict, boarding_type: str) -> dict:
    if boarding_type == "in":
        deck = decklist.get("sideboard")
    elif boarding_type == "out":
        deck = decklist.get("maindeck")
    else:
        raise ValueError("boarding_type must be either 'in' or 'out'")
    print(f"How many of each card are you boarding {boarding_type.upper()} vs. {opp}?")
    result = {}
    for k, v in deck.items():  # type: ignore
        try:
            amount = int(input(f"{k} [0-{v}]: "))
        except ValueError:
            amount = 0
        if amount > 0:
            result[k] = amount
    return result


def full_boarding_for_matchup(opponent_deck: str, decklist: dict) -> dict:
    result_dict = {
        "opponent": opponent_deck,
        "cards_coming_in": boarding(opponent_deck, decklist, "in"),  # type: ignore
        "cards_going_out": boarding(opponent_deck, decklist, "out"),  # type: ignore
    }
    return result_dict


if __name__ == "__main__":
    decklist_location = input("Enter decklist location (eg.: input/shadow.json): ")
    with open(decklist_location, "r") as f:
        decklist_uuid = input(
            "Enter existing UUID to continue boarding creation (ENTER to start fresh): "
        )
        decklist = json.loads(f.read()).get("decklist")
        if decklist_uuid == "":
            decklist_input_data = {
                "deckname": input("Enter deck name: "),  # type: ignore
                "maindeck": decklist.get("maindeck"),
                "sideboard": decklist.get("sideboard"),
                "screen_names": ask_for_screennames(decklist),
            }
            # post decklist to api
            r = requests.post(
                "http://localhost:8000/decklists/json", json=decklist_input_data
            )
            decklist_uuid = r.json().get("id")
            print(f"Decklist created with UUID {decklist_uuid}")
        while True:
            opponent_deck = input("Enter opponent deck (EXIT to finish): ")
            if opponent_deck == "EXIT":
                break
            boarding_dict = full_boarding_for_matchup(opponent_deck, decklist)
            boarding_dict["deckname"] = "Death's Shadow"
            boarding_dict["on_the_play"] = True
            r = requests.post("http://localhost:8000/boardings", json=boarding_dict)
