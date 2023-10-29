import json


def table_header() -> str:
    return "deck\topponent\tcard\tmaindeck\tdelta\n"


def read_json(path: str) -> dict:
    with open(path, "r") as f:
        return json.load(f)


def save_to_txt(filename: str, content: str) -> None:
    with open(filename, "w") as f:
        f.write(content)


def boarding_out(
    our_deck: str, opponent_deck: str, cards: dict, screennames: dict
) -> str:
    result = ""
    for k, v in cards.items():
        try:
            result += f"{our_deck}\t{opponent_deck}\t{screennames[k]}\t1\t-{v}\n"
        except KeyError:
            result += f"{our_deck}\t{opponent_deck}\t{k}\t1\t-{v}\n"
    return result


def boarding_in(
    our_deck: str, opponent_deck: str, cards: dict, screennames: dict
) -> str:
    result = ""
    for k, v in cards.items():
        try:
            result += f"{our_deck}\t{opponent_deck}\t{screennames[k]}\t0\t+{v}\n"
        except KeyError:
            result += f"{our_deck}\t{opponent_deck}\t{k}\t0\t+{v}\n"
    return result


if __name__ == "__main__":
    data = read_json("sideboards.json")
    result_string = table_header()
    print(f"Formatting deck <{data['title']}> by {data['author']}")
    # iterate all matchups
    for k, v in data["matchups"].items():
        result_string += boarding_out(
            data["title"], k, v["play"]["out"], data["screen_names"]
        )
        result_string += boarding_in(
            data["title"], k, v["play"]["in"], data["screen_names"]
        )
        result_string += "\n"
    # save result to file
    save_to_txt("sideboards.txt", result_string)
