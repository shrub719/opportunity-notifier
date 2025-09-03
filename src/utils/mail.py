import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class Message():
    def __init__(self, to_addr, from_addr, from_pass, version):
        self.to_addr = to_addr
        self.from_addr = from_addr
        self.__from_pass = from_pass

        self.version = version
        self.text_content = []
        self.html_content = []
        self.message = MIMEMultipart("alternative")
        self.message["From"] = self.from_addr
        self.message["To"] = self.to_addr

    def append(self, text, html):
        pass

    def end(self):
        text = "\n\n".join(self.text_content)
        html = "\n\n".join(self.html_content)

        self.message["Subject"] = ""
        self.message.attach(MIMEText(text, "plain"))
        self.message.attach(MIMEText(html, "html"))

    def send(self):
        port = 465
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login(self.from_addr, self.__from_pass)
            server.sendmail(self.from_addr, self.to_addr, self.message.as_string())
