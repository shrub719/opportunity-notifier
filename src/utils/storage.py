import json

FILE_NAME = "entries.json"

def load():
    try:
        with open(FILE_NAME, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
        with open(FILE_NAME, "x") as f:
            f.write("{}")

    return data

def save(data):
    with open(FILE_NAME, "w") as f:
        json.dump(data, f, indent=2)
