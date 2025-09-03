from utils import scraper, storage, mail, formatter
import os
from dotenv import load_dotenv


data = storage.load()

load_dotenv()
to_addr = os.getenv("TO_EMAIL")
from_addr = os.getenv("FROM_EMAIL")
from_pass = os.getenv("FROM_PASS")
message = mail.Message(
    to_addr, from_addr, from_pass,
    version="1.0.0-beta"
)

for site in scraper.sites:
    entries = site.scrape()

    send = True
    if site.id not in data:
        data[site.id] = {}
        send = False

    new_entries = []
    for id, entry in entries.items():
        if id not in data[site.id]:
            new_entries.append(entry)
            data[site.id][id] = entry

    if send:
        text = formatter.format_text(new_entries, site.name)
        html = formatter.format_html(new_entries, site.name, site.color)
        message.append(text, html)

message.end()
message.send()

storage.save(data)
