import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

with open("style.css", "r") as f:
    style = f.read()

TEXT_TOP = """Sixth Sense\n\n"""
TEXT_BOTTOM = """\n\n[Version {}]"""

HTML_TOP = f"""<html>
<head>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900&family=Rubik:ital,wght@0,300..900;1,300..900&display=swap" rel="stylesheet">
<style>
{style}
</style
</head>
<body>
<header>Sixth Sense</header>\n"""

HTML_BOTTOM = """\n<footer>Version {}</footer>
</body>
</html>"""


class Message():
    def __init__(self, to_addr, from_addr, from_pass, version):
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.__from_pass = from_pass

        self.version = version
        self.count = 0
        self.text_content = []
        self.html_content = []
        self.message = MIMEMultipart("alternative")
        self.message["From"] = self.from_addr
        self.message["To"] = self.to_addr

    def append(self, text, html):
        pass

    def end(self):
        text = (TEXT_TOP
                + "\n\n".join(self.text_content)
                + TEXT_BOTTOM.format(self.version))
        html = (HTML_TOP
                + "\n".join(self.html_content)
                + HTML_BOTTOM.format(self.version))

        self.message.attach(MIMEText(text, "plain"))
        self.message.attach(MIMEText(html, "html"))

        if self.count == 1:
            subject = "1 New Entry"  # TODO: replace subjects
        else:
            subject = f"{self.count} New Entries"
        self.message["Subject"] = subject

    def send(self):
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.from_addr, self.__from_pass)
            server.sendmail(self.from_addr, self.to_addr, self.message.as_string())
