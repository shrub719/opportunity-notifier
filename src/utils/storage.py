import json

def load(file_name):
    try:
        with open(file_name, "r") as f:
            data = json.load(f)
    except FileNotFoundError:
        data = {}
        with open(file_name, "x") as f:
            f.write("{}")

    return data

def save(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=2)
