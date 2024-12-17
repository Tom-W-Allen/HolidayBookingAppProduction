from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
import ssl
from common.EmailAuthentication import EmailAuthenticationDetails

def get_email_authentication_details():
    load_dotenv()
    password = os.getenv("EMAIL_PASSWORD")
    sender = os.getenv("SENDER")
    server_url = os.getenv("SERVER_URL")

    return EmailAuthenticationDetails(password, sender, server_url)

def send_email(content, recipient, subject, authentication_details):

    # Function based on solution from (ThePyCoach, 2022): https://www.youtube.com/watch?v=g_j6ILT-X0k

    password = authentication_details.password
    sender = authentication_details.sender

    context = ssl.create_default_context()

    message =EmailMessage()
    message.set_content(content)
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = recipient

    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender, password=password)
        server.sendmail(sender, recipient, message.as_string())

def validate_email_address(email):
    at_count = len([char for char in email if char == "@"])

    if at_count != 1:
        return False

    split_address = email.split("@")
    split_by_dot = split_address[1].split(".")

    if len(split_by_dot) != 2:
        return False

    return True