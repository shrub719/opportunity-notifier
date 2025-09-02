from utils import scraper, storage, mail, formatter

data = storage.load()
message = mail.Message(version="1.0.0-beta")

for site in scraper.sites:
    site_data = data[site.id]
    entries, site_data = site.scrape(site_data)
    data[site.id] = site_data

    text = formatter.format_text(entries, site.name, site.color)
    html = formatter.format_html(entries, site.name, site.color)
    message.append(text, html)

message.end()
message.send()

storage.save(data)
