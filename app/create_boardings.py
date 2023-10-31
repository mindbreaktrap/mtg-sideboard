import json


def boarding_in(opp: str, sideboard: dict) -> dict:
    print("How many of each card are you bringing in?")
    print(f"Opponent deck: {opp}")
    result = {"in": {}}
    for k, v in sideboard.items():
        amount = int(input(f"{k} [0-{v}]: "))
        if amount > 0:
            result["in"][k] = amount
    return result


def boarding_out(opp: str, maindeck: dict) -> dict:
    return maindeck


if __name__ == "__main__":
    print("This is a module, not a script.")
    print("Debugging...")
    mb = {}
    sb = {}
    with open("input/shadow.json", "r") as f:
        tmp_dict = json.loads(f.read())
        mb = tmp_dict.get("decklist").get("maindeck")
        sb = tmp_dict.get("decklist").get("sideboard")
    opponent_deck = input("Enter opponent deck: ")
    print(boarding_in(opponent_deck, sb))
    print(boarding_out(opponent_deck, mb))
