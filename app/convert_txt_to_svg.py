import pandas as pd
from IPython.display import SVG
from jinja2 import Environment, FileSystemLoader


def read_data_into_dataframe(path: str) -> pd.DataFrame:
    """Reads the data from the txt file into a dataframe."""
    return pd.read_table(
        path,
        index_col=["card", "maindeck"],
        dtype={"delta": str},
        skip_blank_lines=True,
    )


def pivot_and_filter(deckname: str, dataframe: pd.DataFrame) -> pd.DataFrame:
    """Pivots the dataframe and filters the rows to only include the deckname."""
    mt = dataframe[dataframe.deck == deckname].pivot_table(
        index=["card", "maindeck"],
        columns="opponent",
        values="delta",
        fill_value="",
        aggfunc=lambda x: " ".join(str(v) for v in x),
    )  # Override the aggfunc to work with strings

    mt = (
        mt.reset_index()
        .sort_values(by=["maindeck", "card"], ascending=[False, True])
        .drop("maindeck", axis=1)
        .reset_index(drop=True)
    )
    return mt


def create_svg_from_dataframe(deckname: str, dataframe: pd.DataFrame) -> SVG:
    """Creates the SVG from the dataframe."""
    env = Environment(loader=FileSystemLoader("input"))
    template = env.get_template("template.svg")
    template_vars = {
        "deck_title": deckname,
        "cards": dataframe["card"].tolist(),
        "decks": dataframe.columns.values.tolist()[
            1:
        ],  # Using slice to exclude the column 'cards'
        "data": dataframe.to_dict(),  # Deck name will be the index
    }

    svg = template.render(template_vars)
    return SVG(data=svg)


def txt_to_svg(filepath: str) -> None:
    """Converts the txt file to an SVG using the helperfunctions."""
    df = read_data_into_dataframe(filepath)
    df = pivot_and_filter("Death and Taxes", df)
    svg = create_svg_from_dataframe("Death and Taxes", df)
    # save svg output to file
    with open("output.svg", "w") as f:
        f.write(svg.data)  # type: ignore


if __name__ == "__main__":
    # read .txt location and default to docs/examples/sideboards.txt if not provided
    filepath = input(
        "Enter filepath to txt file (default: docs/examples/sideboards.txt): "
    )
    if filepath == "":
        filepath = "docs/examples/sideboards.txt"
    txt_to_svg(filepath)
