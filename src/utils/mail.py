import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

class Message():
    def __init__(self, version):
        load_dotenv()
        self.to_addr = os.getenv("TO_EMAIL")
        self.from_addr = os.getenv("FROM_EMAIL")
        self.__from_pass = os.getenv("FROM_PASS")

        self.version = version
        self.text_content = []
        self.html_content = []

    def append(self, text, html):
        pass

    def end(self):
        pass

    def send(self):
        pass