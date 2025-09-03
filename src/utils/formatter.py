def format_text(entries, name):
    pass

def format_html(entries, name, color):
    html = f"<div style='background-color: {color};'>\n<h1>{name}</h1>\n"
    for entry in entries:
        html = html + f"<li>\n<h2>{entry["title"]}</h2>\n"
        for detail in entry["details"]:
            html = html + f"<h3>{detail}</h3>\n"
        html = html + f"<a href='{entry["link"]}'>Link</a>\n</li>\n"
    html = html + "</div>"

    return html
