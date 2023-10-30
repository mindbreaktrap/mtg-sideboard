# Magic: The Gathering Sideboard Tools

## Features

- Convert a MTGO decklist in .txt format to a .json file including display names for cards
- Convert a .json file to a pandas-readable .txt file
- Create a sideboard guide .svg from a correctly formatted .txt file

## Initial idea and credits

Original Jupyter notebook and idea by [Sebastian Proost](https://github.com/sepro).

Refined and extended by [gate/mindbreaktrap](https://github.com/mindbreaktrap).

JSON template by [Tommy Hinks](https://github.com/thinks).

The original notebook turned a .txt file into a .svg using Pandas and a Jinja2 template.
An example can be seen below.

![Example](./docs/examples/dnt.svg "Example Guide")

I extended this idea to use a .json file as the source as that is much more readable and easier to edit.

## Roadmap

I want to make the process of creating the boardings content easier by creating a web interface to input data and validate it.

## Setup and usage

1. `pipenv install --dev --deploy`
2. `pipenv shell`
3. `python app/your_desired_script.py`


