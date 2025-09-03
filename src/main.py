from utils import scraper, storage, mail, formatter

data = storage.load()
message = mail.Message(version="1.0.0-beta")

for site in scraper.sites:
    entries = site.scrape()
    new_entries = []
    for id, entry in entries.items():
        if id not in data[site.id]:
            new_entries.append(entry)
            data[site.id][id] = entry

    text = formatter.format_text(new_entries, site.name)
    html = formatter.format_html(new_entries, site.name, site.color)
    message.append(text, html)

message.end()
message.send()

storage.save(data)
