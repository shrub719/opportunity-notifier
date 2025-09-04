def get_title(entries, name):
    if len(entries) == 1:
        return f"1 New {name} Entry"
    return f"{len(entries)} New {name} Entries"

def format_text(entries, name):
    title = get_title(entries, name)
    underline = "=" * len(title)

    text = f"{title}\n{underline}\n\n"
    for entry in entries:
        text = text + entry["title"] + "\n"
        for detail in entry["details"]:
            text = text + detail + "\n"
        text = text + f"Link: {entry['link']}\n\n"

    return text

def format_html(entries, name, color):
    title = get_title(entries, name)

    html = f"<div>\n<h1 style='background-color: {color};'>{title}</h1>\n<ul>\n"
    for entry in entries:
        html = html + f"<li>\n<h2>{entry["title"]}</h2>\n"
        for detail in entry["details"]:
            html = html + f"<h3>{detail}</h3>\n"
        html = html + f"<a href='{entry["link"]}'><h3>Link</h3></a>\n</li>\n"
    html = html + "</ul>\n</div>"

    return html
