import requests
import json
from bs4 import BeautifulSoup

BASE_URL = "https://uptree.co/"
EVENT_FILE = "events.json"

def get_text(element):
    return element.text.rstrip().lstrip()

def card_to_dict(card):
    return {
        "title": get_text(card.h3),
        "date": get_text(card.h4),
        "location": get_text(card.address),
        "link": "https://uptree.co" + card.a["href"]
    }

try:
    with open(EVENT_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
    with open(EVENT_FILE, "x") as file:
        file.write("{}")

for page_name in ["opportunities", "events"]:
    url = BASE_URL + page_name
    page = requests.get(url)


    soup = BeautifulSoup(page.content, "html.parser")
    cards = soup.find_all("li", class_="listings-card")

    for card in cards:
        id = card.a["href"].split("/")
        id = "/".join(id[1:4])

        if id not in data:
            d = card_to_dict(card)
            data[id] = d

with open(EVENT_FILE, "w") as f:
    json.dump(data, f)
