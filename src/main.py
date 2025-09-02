import mail
import scrapers

for site in scrapers.sites:
    new_events = site.scrape()
