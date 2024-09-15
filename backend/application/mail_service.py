from smtplib import SMTP
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_HOST = "smtp.gmail.com"
SMTP_PORT = 587
SENDER_EMAIL = 'bookmagnet.bm@gmail.com'
SENDER_PASSWORD = 'zciw yhjp mtbg ewzn'


def send_message(to, subject, content_body):
    msg = MIMEMultipart()
    msg["To"] = to
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL
    msg.attach(MIMEText(content_body, 'html'))
    client = SMTP(host=SMTP_HOST, port=SMTP_PORT)
    client.ehlo()
    client.starttls()
    client.login(SENDER_EMAIL, SENDER_PASSWORD)
    client.send_message(msg=msg)
    client.close()

#send_message('midhun@email.com','test','<html><h1>hi</h1></html>')