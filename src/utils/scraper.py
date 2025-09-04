import requests
from bs4 import BeautifulSoup

class Trackr():
    def __init__(self):
        self.name = "Trackr"
        self.id = "trackr"
        self.color = "#00798c"

    def scrape(self):
        entries = {"trackr/test": {
            "title": "Test",
            "details": [],
            "link": "about:blank"
        }}

        return entries

class Uptree():
    def __init__(self):
        self.name = "Uptree"
        self.id = "uptree"
        self.color = "#00d391"

    @staticmethod
    def _get_text(element):
        return element.text.rstrip().lstrip()

    def _card_to_dict(self, card):
        return {
            "title": self._get_text(card.h3),
            "details": [
                self._get_text(card.h4),
                self._get_text(card.address)
            ],
            "link": "https://uptree.co" + card.a["href"]
        }

    def scrape(self):
        entries = {}

        for page_name in ["opportunities", "events"]:
            url = "https://uptree.co/" + page_name
            page = requests.get(url)

            soup = BeautifulSoup(page.content, "html.parser")
            cards = soup.find_all("li", class_="listings-card")

            for card in cards:
                id = card.a["href"].split("/")
                id = self.id + "/" + "/".join(id[1:4])
                d = self._card_to_dict(card)
                entries[id] = d

        return entries

sites = [
    Uptree(),
    Trackr()
]