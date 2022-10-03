import logging
import smtplib
import mimetypes
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from datetime import date

date_today = date.today()
file_requests = 'requests.txt'

DEFAULT_FROM_EMAIL = "smtp.google.com"
SERVER_EMAIL = "adress_example@gmail.com"
EMAIL_HOST = "smtp.google.com"
EMAIL_HOST_USER = "adress_example@gmail.com"
EMAIL_HOST_PASSWORD = "12345"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL = 'adress_example@gmail.com'


def send_email():
    smtp = smtplib.SMTP(EMAIL_HOST, EMAIL_PORT)
    smtp.starttls()
    smtp.login(SERVER_EMAIL, EMAIL_HOST_PASSWORD)

    ftype, encoding = mimetypes.guess_type(file_requests)
    file_type, subtype = ftype.split("/")
    try:
        msg = MIMEMultipart()
        msg["From"] = EMAIL_HOST_USER
        msg["To"] = EMAIL
        msg["Subject"] = f'Requests from {date_today}'

        with open(f"{file_requests}", "rb") as f:
            file = MIMEBase(file_type, subtype)
            file.set_payload(f.read())
            encoders.encode_base64(file)

        file.add_header('content-disposition', 'attachment', filename=file_requests)
        msg.attach(file)

        smtp.sendmail(EMAIL_HOST_USER, EMAIL, msg.as_string())
        logging.info('The message was sent successfully!')
        print('ok')
        return "The message was sent successfully!"
    except Exception as err:
        print('not ok')
        logging.info(f"Error: {err},  The message wasn't sent successfully!")
        return "The message wasn't sent successfully!"


def main():
    send_email()
