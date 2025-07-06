import os
import requests
from core.config import settings
from utils.colorText import colorText

def send_simple_message(email_to: str, subject: str, body: str):
    mailgun_api_key = settings.MAILGUN_API_KEY
    if not mailgun_api_key:
        print(colorText("Erreur: MAILGUN_API_KEY n'est pas configurée.", "rouge"))
        return

    MAILGUN_DOMAIN = "sandboxd286ea5bd41d473f9dada7406be22d59.mailgun.org"
    SENDER_EMAIL = f"Mailgun Sandbox <postmaster@{MAILGUN_DOMAIN}>"
    try:
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", mailgun_api_key),
            data={"from": SENDER_EMAIL,
                "to": email_to,
                "subject": subject,
                "text": body
                }
        )

        response.raise_for_status()
        print(colorText(f"Email sent successfully to {email_to}", "vert_fonce"))
        return response.json()
    except requests.exceptions.RequestException as e:
        print(colorText(f"Failed to send email to {email_to}: {e}", "rouge"))
        return None