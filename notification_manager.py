import requests
from twilio.rest import Client
import smtplib
TWILIO_SID = "ACc9e455e6222f8e25d26efa37367215c5"
TWILIO_APIKEY = "c3050ae83d60588d6f979b61a05aa0e7"
VIRTUAL_TWILIO_NUMBER = "+18176314741"
VERIFIED_NUMBER = "+56995433931"

EMAIL_PROVIDER_SMTP_ADDRESS = "smtp.gmail.com"
MY_EMAIL = "cbqsmtp@gmail.com"
MY_PASSWORD = "osxpvbvolrcsicsi"


class NotificationManager:
    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_APIKEY)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=VIRTUAL_TWILIO_NUMBER,
            to=VERIFIED_NUMBER,
        )
        # Prints if successfully sent.
        print(message.sid)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP(EMAIL_PROVIDER_SMTP_ADDRESS) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:Nuevo vuelo en oferta!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )