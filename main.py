import requests
import json
import smtplib, ssl
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# TODO:
#  - email new opportunities.. to a subscription list?
#  - large file optimisations: only read IDs, don't rewrite whole file (low priority)

load_dotenv()
TO_EMAIL = os.getenv("TO_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_PASS = os.getenv("FROM_PASS")

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

def display_event(d):
    return f"{d["title"]}\n{d["date"]}\n{d["location"]}\n{d["link"]}\n"

try:
    with open(EVENT_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
    with open(EVENT_FILE, "x") as file:
        file.write("{}")

new_events = []


# ===== Scrape site ======

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
            e = display_event(d)
            data[id] = d
            new_events.append(e)

# ===== Save/email results =====

if new_events:
    with open(EVENT_FILE, "w") as f:
        json.dump(data, f)

    content = "Subject: New Uptree Events\n\n" + "\n".join(new_events)
    print(content)

    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(FROM_EMAIL, FROM_PASS)
        server.sendmail(FROM_EMAIL, TO_EMAIL, content)
