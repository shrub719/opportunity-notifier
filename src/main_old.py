import requests
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup

# ===== Constants =====

load_dotenv()
TO_EMAIL = os.getenv("TO_EMAIL")
FROM_EMAIL = os.getenv("FROM_EMAIL")
FROM_PASS = os.getenv("FROM_PASS")

BASE_URL = "https://uptree.co/"
EVENT_FILE = "../events.json"
NEW_LINE = "\n"

# ===== Functions =====

def get_text(element):
    return element.text.rstrip().lstrip()

def card_to_dict(card):
    return {
        "title": get_text(card.h3),
        "date": get_text(card.h4),
        "location": get_text(card.address),
        "link": "https://uptree.co" + card.a["href"]
    }

def get_subject(events):
    if len(events) == 1:
        return "1 New Uptree Event"
    return f"{len(events)} New Uptree Events"

def events_to_text(events):
    body = []
    for event in events:
        body.append("\n".join([event["title"], event["date"], event["location"], event["link"]]))
    body = "\n".join(body)

    return body

def events_to_html(events):
    event_list = [
        f"""<a href={event["link"]}>
    <li>
        <h2>{event["title"]}</h2>
        <h3>{event["date"].replace(NEW_LINE, "<br />")}</h3>
        <h4>{event["location"]}</h4>
    </li>
</a>
"""
        for event in events
    ]

    body = f"""<html>
    <head>
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Rubik:ital,wght@0,300..900;1,300..900&display=swap" rel="stylesheet">
        <style>{style}</style
    </head>
    <body>
        <h1>{get_subject(events)}</h1>
        <ul>{NEW_LINE.join(event_list)}</ul>
    </body>
</html>
"""

    return body


# ===== File setup =====

try:
    with open(EVENT_FILE, "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
    with open(EVENT_FILE, "x") as f:
        f.write("{}")

with open("style.css", "r") as f:
    style = f.read()

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
            data[id] = d
            new_events.append(d)

# ===== Save/email results =====

if new_events:
    subject = get_subject(new_events)
    print(subject)

    with open(EVENT_FILE, "w") as f:
        json.dump(data, f)

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = FROM_EMAIL
    message["To"] = TO_EMAIL

    text = events_to_text(new_events)
    html = events_to_html(new_events)
    message.attach(MIMEText(text, "plain"))
    message.attach(MIMEText(html, "html"))

    port = 465
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(FROM_EMAIL, FROM_PASS)
        server.sendmail(FROM_EMAIL, TO_EMAIL, message.as_string())
