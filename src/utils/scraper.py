import requests
from bs4 import BeautifulSoup

class Uptree():
    def __init__(self):
        self.name = "Uptree"
        self.id = "uptree"
        self.color = "#00d391"

    @staticmethod
    def _get_text(element):
        return element.text.rstrip().lstrip()

    def _card_to_dict(self, card, id):
        return {
            "id": id,
            "title": self._get_text(card.h3),
            "date": self._get_text(card.h4),
            "location": self._get_text(card.address),
            "link": "https://uptree.co" + card.a["href"]
        }

    def scrape(self, data):
        entries = []

        for page_name in ["opportunities", "events"]:
            url = "https://uptree.co/" + page_name
            page = requests.get(url)

            soup = BeautifulSoup(page.content, "html.parser")
            cards = soup.find_all("li", class_="listings-card")

            for card in cards:
                id = card.a["href"].split("/")
                id = self.id + "/" + "/".join(id[1:4])
                d = self._card_to_dict(id)
                data[id] = d
                entries.append(d)

        return entries

sites = [
    Uptree
]