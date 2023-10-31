import json


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
        opponent_deck: {
            "notes": input("Enter additional notes for the Matchup: "),
            "play": {
                "in": boarding(opponent_deck, decklist, "in"),  # type: ignore
                "out": boarding(opponent_deck, decklist, "out"),  # type: ignore
            },
        }
    }
    if sum(result_dict[opponent_deck]["play"]["in"].values()) > sum(
        result_dict[opponent_deck]["play"]["out"].values()
    ):
        print("You are boarding more cards in than out. Be careful!")
        return result_dict
    elif sum(result_dict[opponent_deck]["play"]["in"].values()) < sum(
        result_dict[opponent_deck]["play"]["out"].values()
    ):
        raise ValueError("Boarding out more cards than in is not legal. Aborting!")
    else:
        print("Boarding is legal!")
        return result_dict


if __name__ == "__main__":
    print("This is a module, not a script.")
    print("Debugging...")
    with open("input/shadow.json", "r") as f:
        tmp_dict = json.loads(f.read())
        opponent_deck = input("Enter opponent deck (EXIT to finish): ")
        while opponent_deck != "EXIT":
            print(full_boarding_for_matchup(opponent_deck, tmp_dict.get("decklist")))
